## Gerenciamento de Migrações

Para gerenciar as migrações do banco de dados, defina a variável de ambiente:
```bash
$env:FLASK_APP=main.py
```
Crie um ambiente virtual na pasta raíz do projeto:
```bash
python -m venv venv
```
Ative seu ambiente virtual na pasta raíz do projeto:
```bash
.\venv\Scripts\activate
```
Rode o seguinte comando para visualizar o histórico:
```bash
flask db history
```

### Comandos Disponíveis

- Para gerar uma nova migração, é necessário adicionar uma classe em app/models.py com o nome da tabela que deseja criar no banco. Depois disso, digitar o seguinte comando para identificar alterações:  
  ```bash
  flask db migrate
  ```
  E para executar as alterações:
  ```bash
  flask db upgrade
  ```
  


### Histórico

Migração <base> -> 55125547df4a, base de usuários

Atributos:

<li><strong>username</strong>: (string) usuário a ser cadastrado para login</li>
<li><strong>password</strong>: (string) senha vinculada ao usuário</li>

Descrição: Adiciona a tabela 'usuários' ao banco de dados.

Data: 2024-05-25

