## Gerenciamento de Migrações

Para gerenciar as migrações do banco de dados, defina a variável de ambiente:
`$env:FLASK_APP=main.py`

Ative seu ambiente virtual na pasta raíz do projeto:
`.\venv\Scripts\activate`

Rode o seguinte comando para visualizar o histórico:
`flask db history`

### Comandos Disponíveis

- Para gerar uma nova migração, é necessário adicionar uma classe em app/models.py com o nome da tabela que deseja criar no banco. Depois disso, digitar o seguinte comando:  
  `flask db migrate` para identificar alterações  
  `flask db upgrade` para executar as alterações no banco de dados


### Histórico

Migração <base> -> 330b4f1d634e, base de usuários

Descrição: Adiciona a tabela 'usuários' ao banco de dados.

Data: 2024-05-21

