<h1 align="center">Embrapa Vitibrasil API</h1>

<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=CONCLUIDO&color=GREEN&style=for-the-badge"/>
</p>

<p>Esta API Flask permite consultar dados das diferentes abas do site <a href="http://vitibrasil.cnpuv.embrapa.br/index.php">Embrapa Vitibrasil</a>. A API oferece endpoints para acessar informações disponíveis em cada aba e sub-aba do site. A API também possui método de autenticação <b>JWT</b> (JSON Web Token) para realizar as requisições.</p>

## Tabela de Conteúdos

- [1. Registro de Usuário](#1-registro-de-usuário)
  - [Exemplo de requisição](#exemplo-de-requisição)
  - [Parâmetros](#parâmetros)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição)
  - [Como realizar uma requisição](#como-realizar-uma-requisição)
- [2. Login do Usuário](#2-login-do-usuário)
  - [Exemplo de requisição](#exemplo-de-requisição-1)
  - [Parâmetros](#parâmetros-1)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-1)
  - [Como realizar uma requisição](#como-realizar-uma-requisição-1)
- [3. Dados de Produção](#3-dados-de-produção)
  - [Exemplo de requisição](#exemplo-de-requisição-2)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-2)
  - [Como realizar uma requisição](#como-realizar-uma-requisição-2)
- [4. Dados de Processamento](#4-dados-de-processamento)
  - [Exemplo de requisição](#exemplo-de-requisição-3)
  - [Parâmetros](#parâmetros-2)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-3)
  - [Como realizar uma requisição](#como-fazer-uma-requisição)
- [5. Dados de Comercialização](#5-dados-de-comercialização)
  - [Exemplo de requisição](#exemplo-de-requisição-4)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-4)
  - [Como realizar uma requisição](#como-fazer-uma-requisição-1)
- [6. Dados de Importação](#6-dados-de-importação)
  - [Exemplo de requisição](#exemplo-de-requisição-5)
  - [Parâmetros](#parâmetros-3)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-5)
  - [Como fazer uma requisição](#como-fazer-uma-requisição-2)
- [7. Dados de Exportação](#7-dados-de-exportação)
  - [Exemplo de requisição](#exemplo-de-requisição-6)
  - [Parâmetros](#parâmetros-4)
  - [Possíveis respostas da requisição](#possíveis-respostas-da-requisição-6)
  - [Como fazer uma requisição](#como-fazer-uma-requisição-3)
- [Pré-requisitos](#pré-requisitos)
  - [Variáveis .env](#variáveis-env)
- [Como rodar a aplicação](#como-rodar-a-aplicação)
  - [Clonando o repositório](#clonando-o-repositório)
  - [Criando o database](#criando-o-database)
  - [Definindo variáveis de ambiente e ativando virtualenv](#definindo-variáveis-de-ambiente-e-ativando-virtualenv)
  - [Instalando bibliotecas com pip](#instalando-bibliotecas-com-pip)
  - [Criando a base de dados de usuários para acesso à aplicação](#criando-a-base-de-dados-de-usuários-para-acesso-à-aplicação)
  - [Rodando a aplicação](#rodando-a-aplicação)
- [Autores](#autores)


<h2> Endpoints disponíveis </h2>

### 1. Registro de Usuário

<p>Registra usuários no banco de dados. O usuário será usado na autenticação JWT para realizar as requisições GET na API. </p>
<ul>
    <li><strong>Endpoint:</strong> <code>/auth/register</code></li>
    <li><strong>Método:</strong> POST</li>
    <li><strong>Descrição:</strong> Retorna a mensagem de usuário criado ou se usuário existente.</li>
</ul>

##### Exemplo de requisição:
<pre><code>POST /auth/register</code></pre>

##### Parâmetros:
<ul>
    <li><code>username</code>: (string) O usuário para realizar login na API.</li>
</ul>
<ul>
    <li><code>password</code>: (string) A senha que será vinculada ao usuário criado.</li>
</ul>


##### Possíveis respostas da requisição:
<ul>
  <strong>201:</strong> Requisição de criação de recurso concluída com sucesso.
</ul>
<pre><code>{
	"msg": "User {{username} } created successfully!"
}
</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>
<pre><code>{
	"msg": "Username already exists"
}
</code></pre>

##### Como realizar uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/register" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }'
```

* Python:
 ```python
import requests

def registra_usuario(username, password):
    url = "http://localhost:5000/auth/register"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
```


### 2. Login do Usuário

Realiza o login a partir do usuário e senha criados na rota `/auth/register`. O login retornará um token de acesso para as demais requisições.
<ul>
    <li><strong>Endpoint:</strong> <code>/auth/login</code></li>
    <li><strong>Método:</strong> POST</li>
    <li><strong>Descrição:</strong> Retorna a mensagem de usuário ou senha incorretos ou o token de acesso.</li>
</ul>

##### Exemplo de requisição:
<pre><code>POST /auth/login</code></pre>

##### Parâmetros:
<ul>
    <li><code>username</code>: (string) O usuário para realizar login na API.</li>
</ul>
<ul>
    <li><code>password</code>: (string) A senha vinculada ao usuário criado.</li>
</ul>


##### Possíveis respostas da requisição:
<ul>
  <strong>200:</strong> Requisição concluída com sucesso.
</ul>
<pre><code>{
	"access_token": {{access_token}}
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Incorrect username or password."
}
</code></pre>



##### Como realizar uma requisição:
* Prompt de Comando:
```bash
(Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua+senha" }').access_token
```

* Python:
 ```python
import requests

def login_e_retorna_token(username, password):
    url = "http://localhost:5000/auth/login"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    token = response.json().get('access_token')
    return token
```


### 3. Dados de Produção

<p>Consulta dados relacionados à produção de vinhos, sucos e derivados do Rio Grande do Sul.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-producao</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de produção dos produtos disponíveis na aba.</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-producao</code></pre>


##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>

<pre><code>{
  "data": [
    {
      "tipo_produto": "vinho de mesa",
      "produto": "tinto",
      "ano": 1970,
      "quantidade_kg": 174224052
    },
    {
      "tipo_produto": "vinho de mesa",
      "produto": "branco",
      "ano": 1970,
      "quantidade_kg": 748400
    }
  ...
  ]
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>
<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>
		
<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>


##### Como realizar uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }' | Select-Object -ExpandProperty access_token | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/api/dados-producao" -Headers @{ "Authorization" = "Bearer $_" } }
```

* Python:
 ```python
import requests
def realiza_requisicao(token):
    url = "http://localhost:5000/api/dados-producao"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

### 4. Dados de Processamento

<p>Consulta dados relacionados ao processamento de viníferas, americanas e híbridas, uvas de mesa e sem classificação..</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-processamento/&lt;arg&gt;</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de processamento baseados no argumento fornecido (<code>viniferas</code>, <code>uvas-de-mesa</code>, <code>americanas-e-hibridas</code> ou <code>sem-classificacao</code>).</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-processamento/viniferas</code></pre>
<pre><code>GET /api/dados-processamento/uvas-de-mesa</code></pre>
<pre><code>GET /api/dados-processamento/americanas-e-hibridas</code></pre>
<pre><code>GET /api/dados-processamento/sem-classificacao</code></pre>


##### Parâmetros:
<ul>
    <li><code>arg</code>: (string) O tipo de dado de processamento que deseja consultar. Pode ser <code>viniferas</code>, <code>uvas-de-mesa</code>, <code>americanas-e-hibridas</code> ou <code>sem-classificacao</code>.</li>
</ul>

##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>

<pre><code>{
  "data": [
    {
      	"ano": "1970",
	"cultivar": "alicante bouschet",
	"quantidade_kg": 0,
	"tipo_cultivar": "tintas"
    },
    {
	"ano": "1970",
	"cultivar": "ancelota",
	"quantidade_kg": 0,
	"tipo_cultivar": "tintas"
    }
  ...
  ]
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>
<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>
		
<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>



##### Como fazer uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }' | Select-Object -ExpandProperty access_token | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/api/dados-processamento/viniferas" -Headers @{ "Authorization" = "Bearer $_" } }
```

* Python:
 ```python
import requests
def realiza_requisicao(token):
    url = "http://localhost:5000/api/dados-processamento/viniferas"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```


#### 5. Dados de Comercialização

<p>Consulta dados relacionados à comercialização de vinhos, sucos e derivados do Rio Grande do Sul.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-comercializacao</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de comercialização dos produtos disponíveis na aba.</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-comercializacao</code></pre>


##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>
<pre><code>{
  "data": [
    {
	"ano": "1970",
	"produto": "  tinto",
	"quantidade_litros": 83300735,
	"tipo_produto": "vinho de mesa"
    },
    {
	"ano": "1970",
	"produto": "  rosado",
	"quantidade_litros": 107681,
	"tipo_produto": "vinho de mesa"
    }
  ...
  ]
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>
<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>
		
<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>

##### Como fazer uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }' | Select-Object -ExpandProperty access_token | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/api/dados-comercializacao" -Headers @{ "Authorization" = "Bearer $_" } }
```

* Python:
 ```python
import requests
def realiza_requisicao(token):
    url = "http://localhost:5000/api/dados-comercializacao"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

### 6. Dados de Importação

<p>Consulta dados relacionados à importação de vinhos de mesa, espumantes, uvas frescas, uvas passas e sucos de uva.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-importacao/&lt;arg&gt;</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de importação baseados no argumento fornecido (<code>vinhos-de-mesa</code>, <code>espumantes</code>, <code>uvas-frescas</code>, <code>uvas-passas</code> ou <code>sucos-de-uva</code>).</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-importacao/vinhos-de-mesa</code></pre>
<pre><code>GET /api/dados-importacao/espumantes</code></pre>
<pre><code>GET /api/dados-importacao/uvas-frescas</code></pre>
<pre><code>GET /api/dados-importacao/uvas-passas</code></pre>
<pre><code>GET /api/dados-importacao/sucos-de-uva</code></pre>


##### Parâmetros:
<ul>
    <li><code>arg</code>: (string) O tipo de dado de processamento que deseja consultar. Pode ser <code>vinhos-de-mesa</code>, <code>espumantes</code>, <code>uvas-frescas</code>, <code>uvas-passas</code> ou <code>sucos-de-uva</code>.</li>
</ul>



##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>
<pre><code>{
  "data": [
    {
	"ano": 1970,
	"pais": "africa do sul",
	"quantidade_kg": 0,
	"valor_us": 0.0
    },
    {
	"ano": 1970,
	"pais": "alemanha",
	"quantidade_kg": 52297,
	"valor_us": 30498.0
    }
  ...
  ]
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>
<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>
		
<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>

##### Como fazer uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }' | Select-Object -ExpandProperty access_token | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/api/dados-importacao/vinhos-de-mesa" -Headers @{ "Authorization" = "Bearer $_" } }
```

* Python:
 ```python
import requests
def realiza_requisicao(token):
    url = "http://localhost:5000/api/dados-importacao/vinhos-de-mesa"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```


### 7. Dados de Exportação

<p>Consulta dados relacionados à exportação de vinhos de mesa, espumantes, uvas frescas e sucos de uva.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-exportacao/&lt;arg&gt;</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de exportação baseados no argumento fornecido (<code>vinhos-de-mesa</code>, <code>espumantes</code>, <code>uvas-frescas</code> ou <code>sucos-de-uva</code>).</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-exportacao/vinhos-de-mesa</code></pre>
<pre><code>GET /api/dados-exportacao/espumantes</code></pre>
<pre><code>GET /api/dados-exportacao/uvas-frescas</code></pre>
<pre><code>GET /api/dados-exportacao/uvas-passas</code></pre>
<pre><code>GET /api/dados-exportacao/sucos-de-uva</code></pre>


##### Parâmetros:
<ul>
    <li><code>arg</code>: (string) O tipo de dado de processamento que deseja consultar. Pode ser <code>vinhos-de-mesa</code>, <code>espumantes</code>, <code>uvas-frescas</code> ou <code>sucos-de-uva</code>.</li>
</ul>


##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>
<pre><code>{
  "data": [
    {
	"ano": 1970,
	"pais": "afeganistao",
	"quantidade_kg": 0,
	"valor_us": 0
    },
    {
	"ano": 1970,
	"pais": "africa do sul",
	"quantidade_kg": 0,
	"valor_us": 0
    }
  ...
  ]
}
</code></pre>

<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>
<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>
		
<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<ul>
  <strong>400:</strong> Requisição malformada.
</ul>



##### Como fazer uma requisição:
* Prompt de Comando:
```bash
Invoke-RestMethod -Uri "http://localhost:5000/auth/login" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{ "username": "seu_usuario", "password": "sua_senha" }' | Select-Object -ExpandProperty access_token | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/api/dados-exportacao/vinhos-de-mesa" -Headers @{ "Authorization" = "Bearer $_" } }
```

* Python:
 ```python
import requests
def realiza_requisicao(token):
    url = "http://localhost:5000/api/dados-importacao/vinhos-de-mesa"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()
```

<h2>Pré-requisitos</h2>

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [Python](https://www.python.org/downloads/), [MySQL](https://dev.mysql.com/downloads/installer/).
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/) e um um framework para desenvolvimento/teste de API como o [Insomnia](https://insomnia.rest/download).
No projeto, foi utilizado a versão do Python 3.11.9 no Windows 11.

### Variáveis .env
É necessário que você crie um arquivo <b>.env</b> contendo algumas variáveis que serão utilizadas na execução da API. Algumas informações como o host e API_URL podem variar, mas nesse caso, estamos rodando localmente. Esse é um exemplo do arquivo:
```bash
SECRET_KEY = sua_chave_secreta
SQLALCHEMY_DATABASE_URI = mysql://seu_usuario_sql:sua_senha_sql@localhost/seu_database
JWT_SECRET_KEY = jwt_chave_secreta
SQLALCHEMY_TRACK_MODIFICATIONS = False
API_URL = http://localhost:5000
```




<h2>Como rodar a aplicação</h2>

### Clonando o repositório
Clone este repositório:
```
git clone https://github.com/matheus-narracci/challenge_1
```

### Criando o database:
Durante a instalação do MySQL, será configurada uma senha para o usuário <b>root</b> ou um usuário escolhido (opcional). No terminal de comando, acesse o MySQL:
```bash
mysql -u root -p
```
O `-p` pedirá a senha, caso esteja configurada. Esta deve ser inserida assim que o comando for executado.

Assim que fizer o login no MySQL, você pode criar o seu database com o comando SQL e selecioná-lo para utilização com os comandos a seguir:
```bash
CREATE DATABASE seu_database;
USE seu_database;
```

### Definindo variáveis de ambiente e ativando virtualenv

No terminal de comando, acesse o diretório que clonou o repositório:
```bash
cd seu_repositorio
```

Crie uma variável de ambiente da aplicação Flask apontando para o arquivo "main.py":
```bash
$env:FLASK_APP="main.py"
```
Crie um ambiente virtual e ative:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Instalando bibliotecas com pip
Instale as bibliotecas usadas na aplicação:
```bash
pip install -r requirements.txt
```

### Criando a base de dados de usuários para acesso à aplicação
Se quiser começar do 0, remova a pasta "migration" do seu projeto e execute esse comando no terminal:
```bash
flask db init
```
Se quiser permanecer com a pasta, é necessário resetar o arquivo alembic.ini com esse comando antes dos dois últimos :
```bash
flask db stamp head
```
Após seguir uma das opções, execute:
```bash
flask db migrate
```
```bash
flask db upgrade
```
Isso fará com que as classes de `models.py` sejam criadas como tabelas no MySQL.

### Rodando a aplicação
Se todos os comandos acima foram executados com sucesso, sua aplicação está pronta para uso! Execute-a dessa forma:
```bash
flask run
```
Deve ser exibido algo como:
<pre><code> * Serving Flask app 'main.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit</code></pre>

<h2>Autores</h2>

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/viktorferrer"><img src="https://media.licdn.com/dms/image/C4D03AQGrE1fuGDuNqQ/profile-displayphoto-shrink_400_400/0/1648237983102?e=1721865600&v=beta&t=YHS6fsBVaa8NgneIrUU2MnQG-nWCco7_G4wqGe6F660" width="100px;" alt="Viktor Ferrer"/><br /><sub><b>Viktor Ferrer</b></sub></a><br /><a href="https://www.linkedin.com/in/viktor-bartosz-ferrer-7aa1b9196/" title="LinkedIn"><img src="https://github.com/dheereshagrwal/colored-icons/blob/master/public/icons/linkedin/linkedin.svg" width="16"></a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/matheus-narracci"><img src="https://media.licdn.com/dms/image/D4D03AQE0hTYpMS9eEQ/profile-displayphoto-shrink_400_400/0/1676843834758?e=1721865600&v=beta&t=K6XhNaPjrek7npNyCq8TpGP-4wnVkd78i-m5RXH-LAU" width="100px;" alt="Matheus Narracci"/><br /><sub><b>Matheus Narracci</b></sub></a><br /><a href="https://www.linkedin.com/in/matheus-narracci-a5989b160/" title="LinkedIn"><img src="https://github.com/dheereshagrwal/colored-icons/blob/master/public/icons/linkedin/linkedin.svg" width="16"></a></td>
	<td align="center" valign="top" width="14.28%"><a href="https://www.linkedin.com/in/lucas-assis-dias/"><img src="https://media.licdn.com/dms/image/D4D03AQGs1pIBQdGLRQ/profile-displayphoto-shrink_400_400/0/1682109280254?e=1721865600&v=beta&t=sil4cY7GlX85liiZGsVxJtLjReDyS8LtVm35DA1b044" width="100px;" alt="Lucas Assis"/><br /><sub><b>Lucas Assis</b></sub></a><br /><a href="https://www.linkedin.com/in/lucas-assis-dias/" title="LinkedIn"><img src="https://github.com/dheereshagrwal/colored-icons/blob/master/public/icons/linkedin/linkedin.svg" width="16"></a></td>
    </tr>
  </tbody>
</table>

	

