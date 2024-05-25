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
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
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

#### 3. Dados de Processamento

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


##### Exemplo de respostas:
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>

<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>

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


#### 4. Dados de Comercialização

<p>Consulta dados relacionados à comercialização de vinhos, sucos e derivados do Rio Grande do Sul.</p>
<ul>
    <li><strong>Endpoint:</strong> <code>/api/dados-comercializacao</code></li>
    <li><strong>Método:</strong> GET</li>
    <li><strong>Descrição:</strong> Retorna dados de comercialização dos produtos disponíveis na aba.</li>
</ul>

##### Exemplo de requisição:
<pre><code>GET /api/dados-comercializacao</code></pre>

##### Exemplo de respostas:
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>

<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>

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

#### 5. Dados de Importação

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


##### Exemplo de respostas:
<pre><code>{
	"msg": "Missing Authorization Header"
}
</code></pre>

<pre><code>{
	"msg": "Token has expired"
}</code></pre>

<pre><code>{
	"msg": "Missing 'Bearer' type in 'Authorization' header. Expected 'Authorization: Bearer <JWT>'"
}</code></pre>

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



