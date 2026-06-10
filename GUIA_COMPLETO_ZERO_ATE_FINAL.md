# 📖 GUIA COMPLETO: DO ZERO AO FINAL
## Aprenda Python, APIs REST, Autenticação e Deploy

---

## 📑 ÍNDICE

1. [Introdução](#introdução)
2. [O que você vai aprender](#o-que-você-vai-aprender)
3. [Pré-requisitos](#pré-requisitos)
4. [Módulo 1: Conceitos Fundamentais](#módulo-1-conceitos-fundamentais)
5. [Módulo 2: Configuração do Ambiente](#módulo-2-configuração-do-ambiente)
6. [Módulo 3: Entender o Projeto](#módulo-3-entender-o-projeto)
7. [Módulo 4: Rodar o Projeto](#módulo-4-rodar-o-projeto)
8. [Módulo 5: Testar a API](#módulo-5-testar-a-api)
9. [Módulo 6: Entender o Código](#módulo-6-entender-o-código)
10. [Módulo 7: Modificar e Expandir](#módulo-7-modificar-e-expandir)
11. [Módulo 8: Deploy](#módulo-8-deploy)
12. [Apêndices](#apêndices)

---

# INTRODUÇÃO

## Bem-vindo! 👋

Este guia foi criado **especialmente para iniciantes**. Se você:
- ✅ Nunca programou antes
- ✅ Não entende o que é "API"
- ✅ Não sabe o que é "autenticação"
- ✅ Quer aprender de verdade
- ✅ Quer sair do zero para construir coisas reais

**Então você está no lugar certo!**

## Como usar este guia

1. **Leia sequencialmente** - Os módulos aumentam de dificuldade
2. **Execute tudo** - Não pule a prática
3. **Entenda o "por quê"** - Não apenas o "como"
4. **Tome notas** - Escreva suas anotações
5. **Experimente** - Modifique e brinque com o código

---

# O QUE VOCÊ VAI APRENDER

Ao final deste guia, você será capaz de:

✅ Explicar o que é uma API REST  
✅ Entender autenticação e segurança  
✅ Escrever código Python básico  
✅ Usar um banco de dados  
✅ Criptografar senhas com segurança  
✅ Gerar e validar tokens JWT  
✅ Rodar uma aplicação web  
✅ Testar endpoints HTTP  
✅ Fazer deploy em produção  
✅ Criar documentação profissional  

**Tempo total**: 8-10 horas (pode variar)

---

# PRÉ-REQUISITOS

## O que você precisa ter instalado

### 1. Python 3.9+
**O que é?** Linguagem de programação  
**Como verificar se tem:**
```
Abra o terminal/CMD e digite:
python --version
```
**Se não tem:**
- Windows: Baixe em https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

### 2. VS Code (Editor de Código)
**O que é?** Programa para escrever código  
**Baixe em:** https://code.visualstudio.com/

### 3. Git (Opcional mas recomendado)
**O que é?** Sistema de controle de versão  
**Baixe em:** https://git-scm.com/

### 4. MySQL (Banco de Dados)
**O que é?** Sistema para guardar dados  
**Já vem instalado no projeto:** Conecta-se a um servidor remoto

### 5. Postman ou cURL (Para testar)
**O que é?** Ferramentas para testar APIs  
**Postman:** https://www.postman.com/downloads/  
**cURL:** Vem instalado no terminal (Windows 10+)

---

# MÓDULO 1: CONCEITOS FUNDAMENTAIS

Antes de programar, você precisa entender alguns conceitos.

## 1.1 O Que É uma API REST?

### Analogia do Restaurante 🍕

Imagine um restaurante:

```
VOCÊ (Cliente)          GARÇOM (API)          COZINHA (Servidor)
   │                        │                        │
   ├─ Quer comida ────────→ │                        │
   │                        ├─ Pede para cozinha ───→ │
   │                        │                        ├─ Cozinha
   │                        │ ← Comida pronta ────── │
   │ ← Recebe comida ────── │                        │
   │                        │                        │
```

Uma **API REST** funciona assim:

- **Você** = Cliente (seu aplicativo, navegador, Postman)
- **Garçom** = API (FastAPI)
- **Cozinha** = Banco de Dados

### HTTP Methods (Verbos)

As APIs usam "verbos" para dizer o que fazer:

| Verbo | O que faz | Exemplo |
|-------|-----------|---------|
| **GET** | Busca dados | `GET /produtos` → Lista produtos |
| **POST** | Cria dados | `POST /produtos` → Cria novo produto |
| **PUT** | Atualiza dados | `PUT /produtos/1` → Atualiza produto 1 |
| **DELETE** | Deleta dados | `DELETE /produtos/1` → Deleta produto 1 |

### URLs e Endpoints

```
URL: http://localhost:8000/auth/login
     │                     │    │
     └─ Domínio            │    └─ Ação (o que faz)
                           └─ Categoria (agrupamento)
```

## 1.2 Autenticação e JWT

### O Problema

Como o servidor sabe quem você é?

```
Usuário: "Olá! Sou João!"
Servidor: "Como sei que é verdade?"
```

### A Solução: JWT Token

```
1. Você faz login
   ├─ Envia: email + senha
   └─ Recebe: Token secreto (JWT)

2. Você usa o token
   ├─ Envia: Token no header
   └─ Servidor reconhece: "É João!"

3. Token expira
   ├─ Após 30 minutos
   └─ Você precisa fazer login novamente
```

### O que é JWT?

JWT = "Cartão de Identidade Digital"

```
JWT Token = Dados criptografados que o servidor reconhece

Exemplo:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2FvQGV4YW1wbGUuY29tIiwi
ZXhwIjoxNjIzMDA1MDAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Parece confuso, mas é só dados criptografados!

## 1.3 Criptografia de Senhas

### Por que não guardar senha em texto plano?

```
❌ ERRADO:
Banco de Dados:
├─ João: senha123
├─ Maria: abc456
└─ Se hackearem, todos perdem!

✅ CORRETO:
Banco de Dados:
├─ João: $2b$12$h4kK1nZGkL5OwK3dR9M2k.5kL3m9N2o1P0q9R8s7T6u5v4w3x2y1z0
├─ Maria: $2b$12$7nZGkK5lL4mJ6hK8iL9mK.4kL3m9N2o1P0q9R8s7T6u5v4w3x2y1z0
└─ Mesmo que hackearem, não conseguem descobrir as senhas!
```

### Como funciona?

```
BCRYPT = Algoritmo de criptografia super seguro

Senha: "Senha123!"
         ↓
      BCRYPT (com salt aleatório)
         ↓
Hash: $2b$12$.... (irreversível!)

Depois, para verificar:
Usuário digita: "Senha123!"
              ↓
         Compara com BCRYPT
              ↓
         ✅ Senha correta! ou ❌ Senha errada!
```

## 1.4 Banco de Dados (MySQL)

### O que é?

Um programa que guarda dados em tabelas (como Excel, mas mais poderoso).

### Estrutura básica

```
Banco: "prova_saep"
│
├── Tabela: Cliente
│   ├─ ID   | Nome  | Email           | CPF      | Senha
│   ├─ 1    | João  | joao@test.com   | 12345... | $2b$12$...
│   ├─ 2    | Maria | maria@test.com  | 98765... | $2b$12$...
│   └─ 3    | Pedro | pedro@test.com  | 55555... | $2b$12$...
│
├── Tabela: Produto
│   ├─ ID | Nome     | Preço | Validade
│   ├─ 1  | Notebook | 2999  | 31/12/2025
│   ├─ 2  | Mouse    | 49.99 | 31/12/2026
│   └─ 3  | Teclado  | 350   | 31/12/2025
│
└── Tabela: Registro
    ├─ ID | ClienteID | ProdutoID | Data
    ├─ 1  | 1         | 2         | 2024-01-15
    └─ 2  | 2         | 1         | 2024-01-16
```

---

# MÓDULO 2: CONFIGURAÇÃO DO AMBIENTE

Agora vamos preparar seu computador para programar.

## 2.1 Instalar Python

### Windows
1. Abra: https://www.python.org/downloads/
2. Clique no botão grande "Download Python 3.x"
3. Execute o instalador
4. **⚠️ IMPORTANTE:** Marque a caixa "Add Python to PATH"
5. Clique em "Install Now"
6. Aguarde a instalação

### Mac
```bash
brew install python3
```

### Linux
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Verificar instalação
```bash
python --version
# Deve mostrar: Python 3.9+
```

## 2.2 Instalar VS Code

1. Abra: https://code.visualstudio.com/
2. Baixe e instale
3. Abra VS Code
4. Instale extensão "Python" (procure no marketplace)
5. Pronto!

## 2.3 Clonar o Projeto

### Opção 1: Com Git
```bash
git clone https://github.com/seu-usuario/prova-saep.git
cd prova-saep
```

### Opção 2: Manual
1. Baixe os arquivos (ou copie para seu computador)
2. Abra a pasta no VS Code

## 2.4 Criar Ambiente Virtual

**O que é?** Uma "bolha" isolada para o projeto (evita conflitos).

### Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Verificar se funcionou:**
- Seu terminal deve mostrar: `(.venv)` no início

## 2.5 Instalar Dependências

```bash
pip install -r requirements
```

**Espere:** Isso vai baixar todos os pacotes necessários (bcrypt, FastAPI, etc).

---

# MÓDULO 3: ENTENDER O PROJETO

Agora vamos entender o que cada arquivo faz, sem ler código ainda.

## 3.1 Estrutura do Projeto

```
prova-saep/
│
├── 📄 main.py
│   └─ Arquivo principal que "liga" tudo
│
├── 🔐 config.py
│   └─ Segurança (criptografia, JWT)
│
├── ✅ schemas.py
│   └─ Validação de dados (o que pode ser enviado)
│
├── 💾 models/
│   └─ model.py = Tabelas do banco de dados
│
├── 🛣️ routers/
│   ├─ auth_router.py = Endpoints de login/registro
│   └─ prod_router.py = Endpoints de produtos
│
├── 🔧 .env
│   └─ Configurações secretas (senhas, chaves)
│
├── 📋 requirements
│   └─ Lista do que instalar
│
└── 📚 Documentação/
    └─ Vários arquivos .md explicando tudo
```

## 3.2 O que cada arquivo faz (em linguagem simples)

### main.py
**Analogia:** O diretor de uma escola

```
O diretor:
├─ Cria a escola (FastAPI)
├─ Contrata professores (routers)
└─ Liga tudo junto
```

**O que faz:**
- Cria a aplicação
- Registra os routers
- Fornece documentação automática

### config.py
**Analogia:** O cofre do banco

```
O cofre:
├─ Criptografa senhas (bcrypt)
├─ Cria cartões de identidade (JWT)
└─ Valida cartões
```

**O que faz:**
- Bcrypt: Transforma "senha123" em "$2b$12$..." (irreversível!)
- JWT: Cria tokens que expiram em 30 minutos
- Valida tokens nos endpoints protegidos

### schemas.py
**Analogia:** O vendedor de uma loja

```
O vendedor:
├─ Recebe seu pedido
├─ Valida: "Isso é válido?"
│  ├─ Email tem @? SIM
│  ├─ Senha tem 8 caracteres? SIM
│  ├─ CPF tem números? SIM
└─ Aceita ou rejeita
```

**O que faz:**
- Define o formato esperado dos dados
- Valida email, CPF, senha, etc.
- Impede dados inválidos

### models/model.py
**Analogia:** As prateleiras da loja

```
Prateleira de Clientes:
├─ Coluna: ID
├─ Coluna: Nome
├─ Coluna: Email
├─ Coluna: Senha
└─ Linha: Cada cliente

Prateleira de Produtos:
├─ Coluna: ID
├─ Coluna: Nome
├─ Coluna: Preço
└─ Linha: Cada produto
```

**O que faz:**
- Define as tabelas do banco de dados
- Define colunas (nome, tipo, se pode ser vazio, etc)
- Define relacionamentos

### routers/auth_router.py
**Analogia:** A recepção do hotel

```
Recepção:
├─ Registro: "Bem-vindo, vou te registrar!"
├─ Login: "Qual é seu email? E senha?"
└─ Dados: "Aqui estão seus dados"
```

**O que faz:**
- POST /auth/registro → Cria novo usuário
- POST /auth/login → Faz login, retorna token
- GET /auth/me → Retorna dados do usuário logado

### routers/prod_router.py
**Analogia:** A loja de produtos

```
Loja:
├─ Listar: "Veja todos os produtos"
├─ Criar: "Vou adicionar um novo produto"
├─ Atualizar: "Vou mudar o preço"
└─ Deletar: "Vou remover um produto"
```

**O que faz:**
- GET /produto/listar_produtos → Lista todos
- POST /produto/criar_produto → Cria novo
- PUT /produto/atualizar_produto/{id} → Atualiza
- DELETE /produto/deletar_produto/{id} → Deleta

### .env
**Analogia:** O cofre pessoal

```
Cofre contém:
├─ DB_NAME = Nome do banco
├─ DB_USER = Usuário
├─ DB_PASSWORD = Senha
├─ SECRET_KEY = Chave secreta para JWT
└─ Tudo muito secreto!
```

**O que faz:**
- Guarda senhas e chaves secretas
- **NUNCA commita no Git** (ficaria público!)

---

# MÓDULO 4: RODAR O PROJETO

Agora vamos fazer a aplicação funcionar!

## 4.1 Passo a Passo

### Passo 1: Abra o Terminal

No VS Code:
- Pressione: `Ctrl + ~` (acento grave)
- Ou vá em: Terminal → New Terminal

### Passo 2: Ative o Ambiente Virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

Seu terminal deve mostrar `(.venv)` no início da linha.

### Passo 3: Execute a Aplicação

```bash
uvicorn main:app --reload
```

**O que significa:**
- `uvicorn` = Servidor web
- `main:app` = Arquivo `main.py`, variável `app`
- `--reload` = Reinicia quando você salva arquivos

### Passo 4: Veja a mensagem de sucesso

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Pronto!** A aplicação está rodando! 🎉

## 4.2 Acessar a Documentação

Abra seu navegador e vá para:

```
http://localhost:8000/docs
```

Você verá:
- Uma lista de todos os endpoints (rotas)
- Documentação automática (Swagger)
- Um botão "Try it out" para testar cada um

**Parabéns!** Você tem uma API funcional! 🚀

## 4.3 Parar a Aplicação

No terminal, pressione: `Ctrl + C`

---

# MÓDULO 5: TESTAR A API

Agora vamos entender como usar a API e testar cada endpoint.

## 5.1 Conceitos Básicos de Testes

### O que é um endpoint?

Um endpoint é um "ponto de entrada" da API. Exemplo:

```
POST /auth/registro

POST      = tipo de requisição (ação)
/auth     = categoria
/registro = ação específica
```

### Anatomia de uma requisição HTTP

```
POST /auth/login HTTP/1.1
│    │              │
│    │              └─ Versão HTTP
│    └─ Rota (onde)
└─ Método (o quê)

Headers (informações extras):
├─ Content-Type: application/json
└─ Authorization: Bearer token123...

Body (dados que você envia):
{
  "email": "joao@example.com",
  "senha": "Senha123!"
}
```

### Anatomia de uma resposta HTTP

```
HTTP/1.1 200 OK
│        │
│        └─ Status (sucesso/erro)
└─ Versão

Headers:
├─ Content-Type: application/json
└─ Content-Length: 256

Body (dados que você recebe):
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "usuario": {...}
}
```

## 5.2 Status Codes (Códigos de Resposta)

| Código | Significado | Exemplo |
|--------|-------------|---------|
| **200** | Sucesso | Dados retornados corretamente |
| **201** | Criado | Novo item criado com sucesso |
| **400** | Erro de cliente | Email inválido, senha muito curta |
| **401** | Não autenticado | Token inválido ou expirado |
| **404** | Não encontrado | Produto ID 999 não existe |
| **500** | Erro do servidor | Algo deu errado no servidor |

## 5.3 Teste 1: Registrar um Usuário

### Via Swagger (Interface gráfica)

1. Abra: http://localhost:8000/docs
2. Procure por: `POST /auth/registro`
3. Clique em "Try it out"
4. Preencha os dados:
   ```json
   {
     "nome": "João Silva",
     "email": "joao@example.com",
     "telefone": "11999999999",
     "cpf": "12345678901",
     "senha": "Senha123!"
   }
   ```
5. Clique em "Execute"
6. Veja a resposta (deve ser 200 OK)

### Via cURL (Terminal)

```bash
curl -X POST "http://localhost:8000/auth/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "senha": "Senha123!"
  }'
```

### Resposta esperada:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "vip": false
  }
}
```

**O que aconteceu:**
1. Você enviou dados para `/auth/registro`
2. O servidor validou os dados (é um email válido? Senha tem 8 caracteres?)
3. O servidor criptografou a senha com bcrypt
4. O servidor salvou no banco de dados
5. O servidor criou um JWT token
6. O servidor retornou o token + dados do usuário

**Guarde o token!** Você vai usar nos próximos testes.

## 5.4 Teste 2: Fazer Login

### Via Swagger

1. Procure por: `POST /auth/login`
2. Clique em "Try it out"
3. Preencha:
   ```json
   {
     "email": "joao@example.com",
     "senha": "Senha123!"
   }
   ```
4. Execute

### Via cURL

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "Senha123!"
  }'
```

## 5.5 Teste 3: Acessar Endpoint Protegido

### Via Swagger (recomendado)

1. Clique no cadeado 🔒 (no topo direito)
2. Cole seu token (aquele que você guardou)
3. Clique "Authorize"
4. Procure por: `GET /auth/me`
5. Clique em "Try it out"
6. Execute

### Via cURL

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta esperada:**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "11999999999",
  "cpf": "12345678901",
  "vip": false
}
```

## 5.6 Teste 4: Criar um Produto

### Via Swagger

1. Clique no cadeado 🔒 (já deve estar autorizado)
2. Procure por: `POST /produto/criar_produto`
3. Clique em "Try it out"
4. Preencha:
   ```json
   {
     "nome": "Notebook",
     "preco": 2999.99,
     "validade": "31/12/2025"
   }
   ```
5. Execute

**Resposta esperada:**
```json
{
  "id": 1,
  "nome": "Notebook",
  "preco": 2999.99,
  "validade": "31/12/2025"
}
```

## 5.7 Teste 5: Listar Produtos (Público)

### Via Swagger

1. Procure por: `GET /produto/listar_produtos`
2. Clique em "Try it out"
3. Execute (não precisa de token!)

**Resposta esperada:**
```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "preco": 2999.99,
    "validade": "31/12/2025"
  }
]
```

---

# MÓDULO 6: ENTENDER O CÓDIGO

Agora vamos ler o código-fonte e entender como funciona.

## 6.1 O Arquivo Mais Importante: config.py

Este arquivo contém toda a lógica de segurança.

### Bcrypt: Criptografar Senhas

```python
def obter_hash_senha(senha: str) -> str:
    """
    Transforma "Senha123!" em "$2b$12$..."
    Cada execução gera um hash diferente (salt aleatório)
    """
    return pwd_context.hash(senha)

# Exemplo:
senha_texto_plano = "Senha123!"
senha_criptografada = obter_hash_senha(senha_texto_plano)
# Resultado: $2b$12$7nZGkK5lL4mJ6hK8iL9mK...
```

**Por que funciona:**
- Bcrypt usa um "salt" (número aleatório) único
- Mistura a senha + salt
- Criptografa 12 vezes (lento de propósito!)
- Resultado: Impossível descobrir a senha original

### Verificar Senha

```python
def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Compara "Senha123!" com "$2b$12$..."
    Retorna True se igual, False se diferente
    """
    return pwd_context.verify(senha_plana, senha_hash)

# Exemplo:
usuario_digitou = "Senha123!"
senha_no_banco = "$2b$12$7nZGkK5lL4mJ6hK8iL9mK..."
igual = verificar_senha(usuario_digitou, senha_no_banco)
# Resultado: True (são iguais!)
```

### JWT: Criar Tokens

```python
def criar_access_token(data: dict, expires_delta=None):
    """
    Cria um token JWT que expira em 30 minutos
    """
    # Copia os dados
    to_encode = data.copy()
    
    # Define quando expira
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    # Adiciona expiração aos dados
    to_encode.update({"exp": expire})
    
    # Criptografa com a SECRET_KEY (é o que torna único e seguro)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

# Exemplo:
meu_token = criar_access_token({"sub": "joao@example.com"})
# Resultado: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Como funciona:**
1. Pega os dados (email do usuário)
2. Adiciona data de expiração (30 minutos no futuro)
3. Criptografa com SECRET_KEY
4. Retorna um token único que só você pode validar

### JWT: Verificar Token

```python
def verificar_token(credentials):
    """
    Valida se o token é válido e não expirou
    """
    token = credentials.credentials  # Extrai do header
    
    try:
        # Decodifica usando SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")  # Extrai o email
        
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado")

# Exemplo:
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
email = verificar_token(token)
# Resultado: "joao@example.com"
```

**Como funciona:**
1. Recebe o token do header
2. Tenta decodificar com SECRET_KEY
3. Se conseguir e não expirou: retorna o email ✅
4. Se falhar: retorna erro 401 ❌

## 6.2 O Arquivo de Rotas: auth_router.py

Este arquivo define o que cada endpoint faz.

### Endpoint: POST /auth/registro

```python
@router.post('/registro', response_model=Token)
async def registrar_usuario(usuario: ClienteRegistro):
    """
    1. Recebe dados do usuário (nome, email, telefone, cpf, senha)
    2. Valida com Pydantic (email é válido? Senha tem 8 caracteres?)
    3. Verifica: email já existe?
    4. Verifica: CPF já existe?
    5. Criptografa a senha com bcrypt
    6. Salva no banco de dados
    7. Cria JWT token
    8. Retorna token + dados
    """
```

### Endpoint: POST /auth/login

```python
@router.post('/login', response_model=Token)
async def login_usuario(credenciais: Login):
    """
    1. Recebe email + senha
    2. Busca no banco por email
    3. Compara senha com bcrypt.verify()
    4. Se correto: cria JWT token
    5. Se errado: retorna erro 401
    """
```

### Endpoint: GET /auth/me (Protegido)

```python
@router.get('/me', response_model=ClienteResposta)
async def obter_usuario_atual(email: str = Depends(get_current_user_email)):
    """
    1. FastAPI intercepta e valida o token (get_current_user_email)
    2. Se token inválido: erro 401
    3. Se token válido: extrai o email
    4. Busca usuário no banco por email
    5. Retorna dados do usuário
    """
```

**O que é `Depends()`?**
É uma "injeção de dependência" do FastAPI.

```
Você faz: GET /auth/me com token no header
           ↓
FastAPI vê: @router.get(..., email: str = Depends(get_current_user_email))
           ↓
FastAPI chama: get_current_user_email() automaticamente
           ↓
get_current_user_email valida o token
           ↓
Se válido: passa o email para a função
Se inválido: retorna erro 401
```

## 6.3 O Arquivo de Validação: schemas.py

Define o formato esperado dos dados.

### Schema: ClienteRegistro

```python
class ClienteRegistro(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    telefone: str = Field(..., min_length=10, max_length=15)
    cpf: str = Field(..., min_length=11, max_length=14)
    senha: str = Field(..., min_length=8)
```

**O que significa:**
- `nome: str` → Deve ser texto
- `min_length=1, max_length=150` → Entre 1 e 150 caracteres
- `email: EmailStr` → Valida automaticamente se é um email válido
- `...` → Campo obrigatório

**Validação automática:**
```
Usuário envia: {"nome": "", "email": "joao@test", ...}
                         ↓                  ↓
Pydantic valida: nome vazio? ❌  email inválido? ❌
               ↓
FastAPI retorna erro 400: "Dados inválidos"
```

## 6.4 O Arquivo de Banco de Dados: models/model.py

Define as tabelas.

### Tabela: Cliente

```python
class Cliente(Base):
    __tablename__ = 'Cliente'
    
    id = Column(Integer, primary_key=True)        # ID único
    nome = Column(String(150), nullable=False)    # Não pode ser vazio
    email = Column(String(150), unique=True)      # Não pode repetir
    telefone = Column(String(15))
    cpf = Column(String(14), unique=True)         # Não pode repetir
    senha_hash = Column(String(255))              # Hash bcrypt
    vip = Column(Boolean, default=False)          # Padrão: False
```

**O que significa:**
- `primary_key=True` → ID único que identifica cada linha
- `nullable=False` → Não pode ser deixado em branco
- `unique=True` → Não pode haver 2 linhas com o mesmo valor
- `default=False` → Se não informar, usa False

**Exemplo de tabela:**
```
ID | Nome  | Email          | CPF      | SenhaHash       | VIP
1  | João  | joao@test.com  | 123...   | $2b$12$....     | False
2  | Maria | maria@test.com | 456...   | $2b$12$....     | False
3  | Pedro | pedro@test.com | 789...   | $2b$12$....     | True
```

---

# MÓDULO 7: MODIFICAR E EXPANDIR

Agora vamos aprender a modificar o código e adicionar novas funcionalidades.

## 7.1 Mudança Simples: Alterar Expiração do Token

**Arquivo:** `.env`

**Antes:**
```
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Depois:**
```
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Resultado:** Tokens expiram em 60 minutos em vez de 30.

## 7.2 Mudança Simples: Adicionar Novo Campo no Cliente

Vamos adicionar um campo "telefone_alternativo".

### Passo 1: Adicionar na Tabela (models/model.py)

```python
class Cliente(Base):
    __tablename__ = 'Cliente'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True)
    telefone = Column(String(15), nullable=False)
    telefone_alternativo = Column(String(15))  # ← NOVO!
    cpf = Column(String(14), unique=True)
    senha_hash = Column(String(255))
    vip = Column(Boolean, default=False)
```

### Passo 2: Adicionar no Schema (schemas.py)

```python
class ClienteBase(BaseModel):
    nome: str = Field(..., max_length=150)
    email: EmailStr
    telefone: str = Field(..., max_length=15)
    telefone_alternativo: str = Field(None, max_length=15)  # ← NOVO!
    cpf: str = Field(..., max_length=14)
```

### Passo 3: Criar Migração (para atualizar o banco)

```bash
alembic revision --autogenerate -m "Add telefone_alternativo"
alembic upgrade head
```

### Passo 4: Pronto!

Agora você pode registrar usuários com telefone alternativo:

```json
{
  "nome": "João",
  "email": "joao@test.com",
  "telefone": "11999999999",
  "telefone_alternativo": "11988888888",
  "cpf": "12345678901",
  "senha": "Senha123!"
}
```

## 7.3 Adicionar Novo Endpoint: Obter Todos os Usuários VIP

### Passo 1: Adicionar no auth_router.py

```python
from fastapi import APIRouter, HTTPException, Depends

@router.get('/listar_usuarios_vip', response_model=list[ClienteResposta])
async def listar_usuarios_vip(email: str = Depends(get_current_user_email)):
    """
    Lista apenas usuários VIP (requer autenticação)
    """
    session = SessionLocal()
    try:
        # Busca todos os clientes com vip=True
        usuarios_vip = session.query(Cliente).filter(Cliente.vip == True).all()
        
        # Converte para response model
        return [ClienteResposta.from_orm(u) for u in usuarios_vip]
    finally:
        session.close()
```

### Passo 2: Pronto!

Novo endpoint criado:

```bash
GET /auth/listar_usuarios_vip
Header: Authorization: Bearer seu_token
```

Retorna: `[{id: 1, nome: "Pedro", ...}, ...]`

## 7.4 Adicionar Novo Endpoint: Atualizar Usuário

```python
@router.put('/atualizar_usuario/{usuario_id}', response_model=ClienteResposta)
async def atualizar_usuario(
    usuario_id: int,
    dados: ClienteAtualizar,
    email_autenticado: str = Depends(get_current_user_email)
):
    """
    Atualiza dados do usuário (requer autenticação)
    """
    session = SessionLocal()
    try:
        # Busca o usuário
        usuario = session.query(Cliente).filter(Cliente.id == usuario_id).first()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Atualiza apenas os campos enviados
        if dados.nome is not None:
            usuario.nome = dados.nome
        if dados.telefone is not None:
            usuario.telefone = dados.telefone
        
        # Salva
        session.commit()
        session.refresh(usuario)
        
        return ClienteResposta.from_orm(usuario)
    finally:
        session.close()
```

## 7.5 Testando Suas Mudanças

1. Salve os arquivos
2. A aplicação reinicia automaticamente (--reload)
3. Abra: http://localhost:8000/docs
4. Procure pelo novo endpoint
5. Clique em "Try it out" e teste

---

# MÓDULO 8: DEPLOY

Agora vamos colocar sua API em produção!

## 8.1 O que é Deploy?

Deploy = Colocar sua aplicação em um servidor público, não só no seu computador.

```
Seu Computador         Internet          Servidor de Produção
    ↓                    ↓                       ↓
main.py          (http://localhost:8000)   http://api.exemplo.com
localhost:8000   (só você vê)         (qualquer um no mundo vê)
```

## 8.2 Opções de Deploy

### Opção 1: Heroku (Recomendado para iniciantes)

**Passo 1:** Crie conta em https://www.heroku.com/

**Passo 2:** Instale Heroku CLI (comando `heroku`)

**Passo 3:** Crie arquivo `Procfile` na raiz:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Passo 4:** Crie arquivo `runtime.txt`:

```
python-3.9.12
```

**Passo 5:** Deploy via Git:

```bash
heroku create seu-app-nome
git push heroku main
```

**Pronto!** Sua API estará em: `https://seu-app-nome.herokuapp.com/docs`

### Opção 2: Railway (Alternativa moderno)

1. Abra: https://railway.app/
2. Conecte seu GitHub
3. Faça deploy com 1 clique
4. Pronto!

### Opção 3: AWS / Azure / Google Cloud (Profissional)

Para empresas grandes com requisitos complexos.

## 8.3 Checklist Antes de Deploy

Antes de colocar em produção:

- [ ] Remova `--reload` (modo desenvolvimento)
- [ ] Altere `SECRET_KEY` para algo seguro e aleatório
- [ ] Use `https://` em vez de `http://`
- [ ] Ative CORS apenas para domínios permitidos
- [ ] Faça backup do banco de dados
- [ ] Configure logs
- [ ] Teste tudo novamente
- [ ] Tenha plano de recuperação se algo der errado

## 8.4 Variáveis de Ambiente em Produção

**Nunca coloque senhas e chaves no código!**

### No `.env` (desenvolvimento):
```
SECRET_KEY=minha-chave-de-desenvolvimento
DB_PASSWORD=senha123
```

### Em Produção:
- Use variáveis de ambiente do servidor
- Heroku: `heroku config:set SECRET_KEY=minha-chave-secura-gerada`
- AWS: Use AWS Secrets Manager
- Azure: Use Azure Key Vault

---

# APÊNDICES

## APÊNDICE A: Glossário de Termos

| Termo | Significado | Exemplo |
|-------|-------------|---------|
| **API** | Interface que permite comunicação entre programas | FastAPI |
| **Endpoint** | Um "ponto de entrada" da API | POST /auth/login |
| **REST** | Estilo de design para APIs | Usa HTTP methods (GET, POST, PUT, DELETE) |
| **JWT** | Token de autenticação | eyJhbGciOiJIUzI1NiI... |
| **Bcrypt** | Algoritmo de criptografia | Transforma senha em hash |
| **Hash** | Transformação irreversível | abc123 → $2b$12$... |
| **Token** | Identificação única e temporária | Cartão de identidade digital |
| **Schema** | Estrutura esperada de dados | Email deve ter @ |
| **Router** | Agrupamento de endpoints relacionados | /auth/*, /produto/* |
| **Dependency** | Função executada automaticamente | Validar token antes do endpoint |
| **ORM** | Converte dados para objetos Python | SQLAlchemy |
| **Migration** | Mudança na estrutura do banco | Adicionar coluna |
| **Criptografia** | Transformar dados em formato ilegível | Senha → Hash |
| **Deploy** | Colocar em servidor de produção | Heroku, AWS |

## APÊNDICE B: Erros Comuns e Soluções

### Erro: "ModuleNotFoundError: No module named 'fastapi'"

**Causa:** Não instalou dependências

**Solução:**
```bash
pip install -r requirements
```

### Erro: "RuntimeError: No such file or directory: '.env'"

**Causa:** Falta arquivo `.env`

**Solução:** Crie `.env` com as variáveis de ambiente

### Erro: "ConnectionError: (pymysql.err.OperationalError)"

**Causa:** Não conseguiu conectar ao MySQL

**Solução:** Verifique credenciais em `.env`

### Erro: "HTTPException: 401 Token inválido"

**Causa:** Token expirou ou é inválido

**Solução:** Faça login novamente para obter novo token

### Erro: "IntegrityError: UNIQUE constraint failed"

**Causa:** Email ou CPF já existem

**Solução:** Use email ou CPF diferentes

## APÊNDICE C: Recursos para Aprender Mais

### Documentação Oficial
- FastAPI: https://fastapi.tiangolo.com/
- Python: https://python.org/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- JWT: https://jwt.io/

### Cursos Online
- Real Python: https://realpython.com/
- freeCodeCamp: https://www.freecodecamp.org/
- Codecademy: https://www.codecademy.com/

### Comunidades
- Stack Overflow: https://stackoverflow.com/
- Reddit: r/Python, r/learnprogramming
- Discord: Python community servers

## APÊNDICE D: Comandos Úteis

### Git
```bash
git init                    # Inicializar repositório
git add .                   # Adicionar todos os arquivos
git commit -m "mensagem"    # Confirmar mudanças
git push                    # Enviar para GitHub
```

### Python
```bash
python --version            # Ver versão
python -m venv .venv        # Criar ambiente virtual
python -c "import sys; print(sys.executable)"  # Ver path do Python
```

### pip
```bash
pip install package         # Instalar pacote
pip uninstall package       # Desinstalar
pip list                    # Listar instalados
pip freeze > requirements   # Salvar lista
```

### FastAPI
```bash
uvicorn main:app --reload                   # Dev
uvicorn main:app --host 0.0.0.0 --port 80  # Produção
```

### cURL
```bash
curl -X GET http://localhost:8000/         # GET
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{...}'  # POST
curl -H "Authorization: Bearer token" http://localhost:8000/auth/me  # Com autenticação
```

## APÊNDICE E: Checklist para Iniciantes

### Semana 1: Instalação e Conceitos
- [ ] Python instalado e funcionando
- [ ] VS Code instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Aplicação rodando em localhost:8000
- [ ] Documentação Swagger acessível

### Semana 2: Entendimento
- [ ] Todos os testes do Módulo 5 funcionando
- [ ] Conceitos de autenticação entendidos
- [ ] JWT e bcrypt explicados
- [ ] Estrutura do projeto clara
- [ ] Código comentado lido

### Semana 3: Modificação
- [ ] Mudanças simples implementadas
- [ ] Novo endpoint criado
- [ ] Campo novo adicionado
- [ ] Testes passando

### Semana 4: Deploy
- [ ] Conta criada em plataforma de deploy
- [ ] Aplicação em produção
- [ ] URL pública acessível
- [ ] Token funciona em produção

## APÊNDICE F: Segurança em Checklist

Antes de usar em produção:

- [ ] SECRET_KEY alterado (gerado com `secrets.token_urlsafe(32)`)
- [ ] DB_PASSWORD em variável de ambiente
- [ ] Sem dados sensíveis em logs
- [ ] HTTPS ativado (não HTTP)
- [ ] CORS configurado (não aceita todos)
- [ ] Rate limiting ativado
- [ ] Senhas validadas (mínimo 8 caracteres)
- [ ] Email validado
- [ ] Testes de segurança executados
- [ ] Backup do banco configurado

## APÊNDICE G: Gerador de SECRET_KEY Segura

```python
import secrets

# Execute uma vez e copie o resultado:
chave_segura = secrets.token_urlsafe(32)
print(chave_segura)

# Resultado exemplo:
# K7mN9kL2pO4qR6sT8uV0wX1yZ2aB3cD4eF5gH6i
```

---

# CONCLUSÃO

## Parabéns! 🎉

Você completou este guia do zero ao final!

Agora você sabe:

✅ O que é uma API REST  
✅ Como funciona autenticação JWT  
✅ Como criptografar senhas com bcrypt  
✅ Como rodar uma aplicação FastAPI  
✅ Como testar endpoints HTTP  
✅ Como ler e entender código Python  
✅ Como modificar e expandir a aplicação  
✅ Como fazer deploy em produção  

## Próximas Etapas

1. **Praticar** - Crie suas próprias APIs
2. **Aprofundar** - Estude conceitos avançados
3. **Contribuir** - Ajude outros iniciantes
4. **Construir** - Crie projetos reais

## Dúvidas?

- Leia a documentação oficial
- Procure no Stack Overflow
- Pergunte em comunidades Python
- Estude o código comentado

---

**Desenvolvido com ❤️ para iniciantes**

**Última atualização:** Junho de 2024

**Versão:** 1.0
