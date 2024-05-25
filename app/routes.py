from app import app, db, jwt
from app.models import Usuarios
from flask import jsonify, Blueprint, request, Flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import pandas as pd
import requests
import io
from unidecode import unidecode

routes = Blueprint('routes', __name__)

@routes.route("/dados-producao")
@jwt_required()
def get_producao():
    try:
        # URL do arquivo CSV
        url = "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv"

        # Fazendo uma solicitação GET para o arquivo CSV
        response = requests.get(url)
        # response.raise_for_status()  # Verifica se houve erro na solicitação
        
        # Lendo os dados do arquivo CSV
        df = pd.read_csv(io.StringIO(response.content.decode('utf8')), sep=';')
        
        # Dropa primeiras colunas - index e coluna "repetida"
        df = df.drop(df.columns[[0, 2]], axis=1)
        # cria coluna produto
        df['produto'] = df['control']
        df = df.drop(columns=['control'])

        # Cria range dos anos presentes na base
        anos = list(range(1970, 2024))

        # Obtemos todos os nomes de coluna, exceto o último
        col_substituir = df.columns[:-1]

        # Substituímos os nomes das colunas exceto a última
        df.rename(columns=dict(zip(col_substituir, anos)), inplace=True)

        # Ajusta colunas
        dados_reestruturados = pd.melt(df, id_vars='produto', var_name='ano', value_name='quantidade_kg')

        # Dropa dados desnecessários - ex: Totais
        dados_reestruturados = dados_reestruturados.drop(dados_reestruturados[dados_reestruturados['produto'].str.isupper()].index)
        # dados_reestruturados[dados_reestruturados['produto'].str.isupper()]['produto']

        # Define nova classificação dos produtos a partir do que foi definido na base de dados, criando uma nova coluna
        dados_reestruturados['tipo_produto'] = dados_reestruturados['produto'].apply(
                                                lambda x: 'vinho de mesa' if 'vm_' in x.lower() 
                                                else ('vinho fino de mesa (vinifera)' if 'vv_' in x.lower() 
                                                    else ('suco' if 'su_' in x.lower() else ('derivado' if 'de_' in x.lower() else 'Outro'))))

        # Exclui o prefixo, deixa em minusculo e retira acentuação
        dados_reestruturados['produto'] = dados_reestruturados['produto'].apply(lambda x: x.split('_')[1]).str.lower().apply(lambda x: unidecode(x))

        # Organiza colunas
        dados_reestruturados = dados_reestruturados[['tipo_produto', 'produto', 'ano', 'quantidade_kg']]

         # Transforma os dados em JSON
        dados_json = dados_reestruturados.to_dict(orient='records')

        # Retorna os dados como resposta
        return jsonify({"data": dados_json})

    except requests.exceptions.RequestException as e:
        # Lidar com erros de solicitação
        return jsonify({"error": "Erro ao fazer a solicitação: " + str(e)}), 500

    except pd.errors.ParserError as e:
        # Lidar com erros ao analisar o arquivo CSV
        return jsonify({"error": "Erro ao analisar o arquivo CSV: " + str(e)}), 500

@routes.route("/dados-processamento/<arg>", methods=['GET'])
@jwt_required()
def get_processa_viniferas(arg):
    # URL do arquivo CSV
    if arg == 'viniferas':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv"
    elif arg == 'americanas-e-hibridas':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaAmericanas.csv"
    elif arg =='uvas-de-mesa':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaMesa.csv"
    elif arg == 'sem-classificacao':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ProcessaSemclass.csv"

    try:
        # Fazendo uma solicitação GET para o arquivo CSV
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na solicitação

        # Lendo os dados do arquivo CSV
        df = pd.read_csv(io.StringIO(response.content.decode('utf8')), sep='\t')
      
        # Deleta colunas
        if arg =='sem-classificacao':
            df = df.drop(columns=['control', 'id'], axis=1)
        else:
            df = df.drop(columns=['cultivar', 'id'], axis=1)

        # Renomeia coluna
        if arg =='sem-classificacao':
            pass
        else:
            df.rename(columns={'control':'cultivar'}, inplace=True)

        # Ajusta colunas
        dados_reestruturados = pd.melt(df, id_vars='cultivar', var_name='ano', value_name='quantidade_kg')

        # Dropa dados desnecessários - ex: Totais
        dados_reestruturados = dados_reestruturados.drop(dados_reestruturados[dados_reestruturados['cultivar'].str.isupper()].index)
        # dados_reestruturados[dados_reestruturados['cultivar'].str.isupper()]['cultivar']

        # Define nova classificação dos produtos a partir do que foi definido na base de dados, criando uma nova coluna
        if arg == 'sem-classificacao':
            dados_reestruturados['tipo_cultivar'] = 'outros'
        elif arg =='uvas-de-mesa':
            dados_reestruturados['tipo_cultivar'] = dados_reestruturados['cultivar'].apply(
                lambda x: 'tintas' if 'ti_' in x.lower() 
                else('brancas' if 'br_' in x.lower() 
                    else 'Outros'))
        else:
            dados_reestruturados['tipo_cultivar'] = dados_reestruturados['cultivar'].apply(
                lambda x: 'tintas' if 'ti_' in x.lower() 
                else('brancas e rosadas' if 'br_' in x.lower() 
                    else 'Outros'))


        # Exclui o prefixo, deixa em minusculo e retira acentuação
        if arg == 'sem-classificacao':
            dados_reestruturados['cultivar'] = dados_reestruturados['cultivar'].str.lower().apply(lambda x: unidecode(x))
        else:
            dados_reestruturados['cultivar'] = dados_reestruturados['cultivar'].apply(lambda x: x.split('_')[1]).str.lower().apply(lambda x: unidecode(x))

         # Transforma os dados em JSON
        dados_json = dados_reestruturados.to_dict(orient='records')

        # Retorna os dados como resposta
        return jsonify({"data": dados_json})
    
    except requests.exceptions.RequestException as e:
        # Lidar com erros de solicitação
        return jsonify({"error": "Erro ao fazer a solicitação: " + str(e)}), 500

    except pd.errors.ParserError as e:
        # Lidar com erros ao analisar o arquivo CSV
        return jsonify({"error": "Erro ao analisar o arquivo CSV: " + str(e)}), 500


@routes.route("/dados-importacao/<arg>", methods=['GET'])
@jwt_required()
def get_importacao(arg):
    # URL do arquivo CSV
    if arg == 'vinhos-de-mesa':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"
    elif arg == 'espumantes':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpEspumantes.csv"
    elif arg == 'uvas-frescas':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpFrescas.csv"
    elif arg == 'uvas-passas':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpPassas.csv"
    elif arg == 'sucos-de-uva':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ImpSuco.csv"


    try:
        # Fazendo uma solicitação GET para o arquivo CSV
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na solicitação

        # Lendo os dados do arquivo CSV
        df = pd.read_csv(io.StringIO(response.content.decode('utf8')), sep=';')

        # Define os anos que deseja processar
        anos = range(1970, 2024)

        # Lista para armazenar os DataFrames derretidos de cada ano
        dfs = []

        # Itera sobre os anos
        for ano in anos:
            # Seleciona as colunas correspondentes ao ano e seu respectivo valor
            coluna_quantidade = str(ano)
            coluna_valor = f"{ano}.1"
            
            # Verifica se ambas as colunas estão presentes no DataFrame
            if coluna_quantidade in df.columns and coluna_valor in df.columns:

                # Seleciona as colunas correspondentes ao ano e seu respectivo valor
                df_ano = df[['País', coluna_quantidade, coluna_valor]]
                
                # Renomeia as colunas para quantidade e valor
                df_ano = df_ano.rename(columns={coluna_quantidade: 'quantidade_kg', coluna_valor: 'valor_us', 'País': 'pais'})
                
                # Adiciona a coluna ano
                df_ano['ano'] = ano
                
                # Adiciona o DataFrame derretido à lista
                dfs.append(df_ano)

        # Concatena os DataFrames derretidos em um único DataFrame
        dados_reestruturados = pd.concat(dfs)

        # Deixa em minusculo e retira acentuação
        dados_reestruturados['pais'] = dados_reestruturados['pais'].str.lower().apply(lambda x: unidecode(x))

        # Transforma os dados em JSON
        dados_json = dados_reestruturados.to_dict(orient='records')

        # Retorna os dados como resposta
        return jsonify({"data": dados_json})
    
    except requests.exceptions.RequestException as e:
        # Lidar com erros de solicitação
        return jsonify({"error": "Erro ao fazer a solicitação: " + str(e)}), 500

    except pd.errors.ParserError as e:
        # Lidar com erros ao analisar o arquivo CSV
        return jsonify({"error": "Erro ao analisar o arquivo CSV: " + str(e)}), 500


@routes.route("/dados-exportacao/<arg>", methods=['GET'])
@jwt_required()
def get_exportacao(arg):
    # URL do arquivo CSV
    if arg == 'vinhos-de-mesa':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
    elif arg == 'espumantes':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv"
    elif arg == 'uvas-frescas':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpUva.csv"
    elif arg == 'sucos-de-uva':
        url = "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"


    try:
        # Fazendo uma solicitação GET para o arquivo CSV
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na solicitação

        # Lendo os dados do arquivo CSV
        df = pd.read_csv(io.StringIO(response.content.decode('utf8')), sep=';')

        # Define os anos que deseja processar
        anos = range(1970, 2024)

        # Lista para armazenar os DataFrames derretidos de cada ano
        dfs = []

        # Itera sobre os anos
        for ano in anos:
            # Seleciona as colunas correspondentes ao ano e seu respectivo valor
            coluna_quantidade = str(ano)
            coluna_valor = f"{ano}.1"
            
            # Verifica se ambas as colunas estão presentes no DataFrame
            if coluna_quantidade in df.columns and coluna_valor in df.columns:

                # Seleciona as colunas correspondentes ao ano e seu respectivo valor
                df_ano = df[['País', coluna_quantidade, coluna_valor]]
                
                # Renomeia as colunas para quantidade e valor
                df_ano = df_ano.rename(columns={coluna_quantidade: 'quantidade_kg', coluna_valor: 'valor_us', 'País': 'pais'})
                
                # Adiciona a coluna ano
                df_ano['ano'] = ano
                
                # Adiciona o DataFrame derretido à lista
                dfs.append(df_ano)

        # Concatena os DataFrames derretidos em um único DataFrame
        dados_reestruturados = pd.concat(dfs)

        # Deixa em minusculo e retira acentuação
        dados_reestruturados['pais'] = dados_reestruturados['pais'].str.lower().apply(lambda x: unidecode(x))

        # Transforma os dados em JSON
        dados_json = dados_reestruturados.to_dict(orient='records')

        # Retorna os dados como resposta
        return jsonify({"data": dados_json})

    except requests.exceptions.RequestException as e:
        # Lidar com erros de solicitação
        return jsonify({"error": "Erro ao fazer a solicitação: " + str(e)}), 500

    except pd.errors.ParserError as e:
        # Lidar com erros ao analisar o arquivo CSV
        return jsonify({"error": "Erro ao analisar o arquivo CSV: " + str(e)}), 500

@routes.route("/dados-comercializacao")
@jwt_required()
def get_comercializacao():
    # URL do arquivo CSV
    url = "http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv"
    
    try:
        # Fazendo uma solicitação GET para o arquivo CSV
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve erro na solicitação
        
        # Lendo os dados do arquivo CSV
        df = pd.read_csv(io.StringIO(response.content.decode('utf8')), sep=';')
        
        # Dropa colunas Id e control
        df = df.drop(df.columns[[0, 1]], axis=1)
        
        # Ajusta as colunas
        dados_reestruturados = pd.melt(df, id_vars='Produto', var_name='ano', value_name='quantidade_litros')

        # Lista para armazenar os tipos
        tipos = []

        # Variável para armazenar o tipo atual
        tipo_atual = None

        # Itera sobre as linhas da coluna 'control'
        for control in dados_reestruturados['Produto']:
            if control.isupper():
                tipo_atual = control
            tipos.append(tipo_atual)

        # Adiciona a nova coluna tipo_produto
        dados_reestruturados['tipo_produto'] = [x.lower() for x in tipos]

        # Remove as linhas que contêm os tipos (caixa alta) da coluna 'Produto'
        dados_reestruturados = dados_reestruturados[~dados_reestruturados['Produto'].str.isupper()]

        # Renomeia a coluna 'produto' para 'subtipo'
        dados_reestruturados = dados_reestruturados.rename(columns={'Produto': 'produto'})
        dados_reestruturados['produto'] = dados_reestruturados['produto'].apply(lambda x : x.lower())

        # Transforma os dados em JSON
        dados_json = dados_reestruturados.to_dict(orient='records')

        # Retorna os dados como resposta
        return jsonify({"data": dados_json})
    
    except requests.exceptions.RequestException as e:
        # Retornando uma mensagem de erro se a solicitação falhar
        return jsonify({"error": str(e)}), 500
    except pd.errors.ParserError as e:
        # Retornando uma mensagem de erro se houver um erro ao analisar o arquivo CSV
        return jsonify({"error": "Erro ao analisar o arquivo CSV"}), 500