<h1 align="center">Embrapa Vitibrasil API</h1>

<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

<p>Esta API permite consultar dados das diferentes abas do site <a href="http://vitibrasil.cnpuv.embrapa.br/index.php">Embrapa Vitibrasil</a>. A API oferece endpoints para acessar informações disponíveis em cada aba e sub-aba do site. A API também possui método de autenticação <b>JWT</b>(JSON Web Token) para realizar as requisições.</p>

<h2> Funcionalidades </h2>

<h3> Endpoints disponíveis </h3>

#### 1. Registro de Usuário

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

##### Exemplo de respostas:
<pre><code>{
	"msg": "User not found."
}
</code></pre>

<pre><code>{
	"msg": "User {{username} } created successfully!"
}
</code></pre>

##### Possíveis respostas da requisição:
<ul>
  <li><strong>201:</strong> Requisição de criação de recurso concluída com sucesso.</li>
</ul>
<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<ul>
  <li><strong>400:</strong> Requisição malformada.</li>
</ul>


##### Exemplos de uso
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


#### 2. Login do Usuário

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

##### Exemplo de respostas:
<pre><code>{
	"msg": "Incorrect username or password."
}
</code></pre>

<pre><code>{
	"access_token": {{access_token}}"
}
</code></pre>

##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>
<ul>
  <li><strong>401:</strong> Credenciais inválidas.</li>
</ul>
<ul>
  <li><strong>400:</strong> Requisição malformada.</li>
</ul>


##### Exemplos de uso
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


#### 3. Dados de Produção

<p>Consulta dados relacionados à produção de vinhos, sucos e derivados do Rio Grande do Sul.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-producao</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de produção dos produtos disponíveis na aba.</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-producao</code></pre>

##### Exemplo de respostas:
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>

<pre><code>{
	"msg": "Token has expired"
}</code></pre>

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

##### Possíveis respostas da requisição:
<ul>
  <li><strong>200:</strong> Requisição concluída com sucesso.</li>
</ul>
<ul>
  <li><strong>401:</strong> Token expirado.</li>
</ul>
<ul>
  <li><strong>400:</strong> Requisição malformada.</li>
</ul>


##### Exemplos de uso
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

