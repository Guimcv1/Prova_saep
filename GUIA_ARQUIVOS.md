# 📖 GUIA COMPLETO - O QUE CADA ARQUIVO FAZ

## 🗂️ ESTRUTURA DO PROJETO

```
Prova_saep/
├── main.py                    ← Aplicação principal (cria app FastAPI)
├── config.py                  ← Segurança (JWT, criptografia, bcrypt)
├── schemas.py                 ← Validação de dados (Pydantic models)
├── .env                       ← Variáveis de ambiente (banco, JWT)
├── requirements               ← Dependências Python
├── README.md                  ← Documentação principal
├── TESTES.md                  ← Exemplos de testes com cURL
├── REFERENCIA_RAPIDA.md       ← Referência rápida
├── GUIA_ARQUIVOS.md          ← Este arquivo
│
├── models/
│   └── model.py               ← Models do banco (Cliente, Produto, Registro)
│
├── routers/
│   ├── auth_router.py         ← Endpoints de autenticação
│   └── prod_router.py         ← Endpoints de produtos
│
└── alembic/                   ← Migrações do banco de dados
    ├── env.py
    ├── script.py.mako
    └── README
```

---

## 📄 DETALHAMENTO DE CADA ARQUIVO

### 🎯 **main.py** - ENTRADA DA APLICAÇÃO
**O que faz:** Cria a aplicação FastAPI e registra os routers.

**Funções principais:**
- Cria instância do FastAPI
- Inclui router de autenticação (`auth_router.py`)
- Inclui router de produtos (`prod_router.py`)
- Define endpoint raiz `/`

**Importâncias:** Sem este arquivo, a aplicação não funciona!

**Como funciona:**
```python
app = FastAPI()  # ← Cria a app
app.include_router(auth_router)  # ← Registra endpoints /auth/*
app.include_router(prod_router)   # ← Registra endpoints /produto/*
```

---

### 🔐 **config.py** - SEGURANÇA E AUTENTICAÇÃO
**O que faz:** Implementa criptografia de senhas (bcrypt) e JWT tokens.

**Funções principais:**

1. **`obter_hash_senha(senha)`**
   - Criptografa senha com bcrypt
   - Retorna hash irreversível e seguro
   - Uso: `hash = obter_hash_senha("minhassenha123")`

2. **`verificar_senha(senha_plana, senha_hash)`**
   - Compara senha digitada com hash armazenado
   - Usa bcrypt para comparação segura
   - Retorna True/False
   - Uso: `if verificar_senha("minha_senha", hash_do_banco):`

3. **`criar_access_token(data, expires_delta)`**
   - Gera JWT token válido por 30 minutos (padrão)
   - Assina com SECRET_KEY do .env
   - Retorna string com token criptografado
   - Uso: `token = criar_access_token({"sub": "email@example.com"})`

4. **`verificar_token(credentials)`**
   - Valida e decodifica JWT token
   - Extrai email do token
   - Retorna email se válido, erro 401 se inválido
   - Uso interno (dependency)

5. **`get_current_user_email(credentials)`** ⭐ IMPORTANTE
   - Dependency para proteger endpoints
   - Extrai e retorna email do usuário autenticado
   - Usa em: `@router.get("/protected", email = Depends(get_current_user_email))`

**Constantes configuradas:**
- `SECRET_KEY` - Chave para assinar JWT (do .env)
- `ALGORITHM` - HS256 (padrão seguro)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - 30 minutos

---

### ✅ **schemas.py** - VALIDAÇÃO DE DADOS
**O que faz:** Define estrutura esperada de dados (Pydantic models).

**Schemas para CLIENTE:**

1. **`ClienteBase`** (classe base)
   - `nome: str` - obrigatório, 1-150 caracteres
   - `email: EmailStr` - valida automaticamente email
   - `telefone: str` - 10-15 caracteres
   - `cpf: str` - 11-14 caracteres

2. **`ClienteRegistro`** (herda ClienteBase + senha)
   - Inclui: `senha: str` (mínimo 8 caracteres)
   - Uso: Dados para `/auth/registro`

3. **`ClienteResposta`** (herda ClienteBase + id + vip)
   - Retorna dados do cliente SEM senha
   - `id: int` - ID gerado no banco
   - `vip: bool` - Status VIP
   - Uso: Respostas de endpoints GET/POST autenticados

4. **`ClienteAtualizar`** (todos campos opcionais)
   - Permite atualização parcial
   - Uso: PUT request para atualizar alguns campos

**Schemas para AUTENTICAÇÃO:**

1. **`Login`**
   - `email: EmailStr` - email do usuário
   - `senha: str` - senha em texto plano
   - Uso: POST `/auth/login`

2. **`Token`** (resposta após login/registro)
   - `access_token: str` - JWT token
   - `token_type: str` - sempre "bearer"
   - `usuario: ClienteResposta` - dados do usuário

3. **`TokenData`** (interno)
   - Dados extraídos do token
   - `email: str` - email do token
   - `exp: datetime` - data de expiração

**Schemas para PRODUTO:**

1. **`ProdutoBase`**
   - `nome: str` - 1-150 caracteres
   - `preco: float` - deve ser > 0
   - `validade: str` - DD/MM/YYYY

2. **`ProdutoResposta`** (herda ProdutoBase + id)
   - Retorna produto com ID
   - Uso: Respostas de endpoints GET/POST

3. **`ProdutoAtualizar`** (todos campos opcionais)
   - Permite atualização parcial
   - Uso: PUT request

**Schemas para REGISTRO:**

1. **`RegistroBase`**
   - `cliente_id: int` - ID do cliente
   - `produto_id: int` - ID do produto

2. **`RegistroResposta`** (herda RegistroBase + id + data)
   - `id: int` - ID do registro
   - `data: datetime` - data/hora da transação

---

### 💾 **models/model.py** - BANCO DE DADOS
**O que faz:** Define estrutura das tabelas do MySQL (SQLAlchemy models).

**Configuração:**
- Lê credenciais do banco do `.env`
- Cria URL: `mysql+pymysql://user:pass@host:port/db`
- Cria engine (gerenciador de conexão)

**Tabelas:**

1. **`Cliente`** (usuários)
   ```
   id (int, PK, auto)          - ID único
   nome (String 150, NOT NULL) - Nome do cliente
   email (String 150, UNIQUE)  - Email único (para login)
   telefone (String 15, NOT NULL) - Telefone
   cpf (String 14, UNIQUE)     - CPF único
   senha_hash (String 255)     - Hash bcrypt da senha
   vip (Boolean, default=False) - Status VIP
   ```

2. **`Produto`** (catálogo)
   ```
   id (int, PK, auto)         - ID único
   nome (String 150)          - Nome do produto
   preco (Float)              - Preço
   validade (String 10)       - Data de validade
   ```

3. **`Registro`** (transações)
   ```
   id (int, PK, auto)         - ID único
   cliente_id (int, FK)       - Referencia Cliente.id
   produto_id (int, FK)       - Referencia Produto.id
   data (DateTime)            - Data/hora da transação
   ```

---

### 🔑 **routers/auth_router.py** - AUTENTICAÇÃO
**O que faz:** Define endpoints para registro, login e gerenciamento de usuários.

**Endpoints:**

1. **`POST /auth/registro`** ✅ SEM autenticação
   - Registra novo usuário
   - Valida: email único, CPF único, senha mínimo 8 caracteres
   - Criptografa senha com bcrypt
   - Gera JWT token automaticamente
   - Retorna: Token + dados do usuário

2. **`POST /auth/login`** ✅ SEM autenticação
   - Faz login com email e senha
   - Verifica credenciais (bcrypt)
   - Gera JWT token
   - Retorna: Token + dados do usuário

3. **`GET /auth/me`** ⚠️ REQUER TOKEN
   - Retorna dados do usuário autenticado
   - Email extraído do token JWT
   - Retorna: ClienteResposta (sem senha)

4. **`GET /auth/listar_usuario`** ⚠️ REQUER TOKEN
   - Lista todos os usuários do sistema
   - Retorna: Lista de ClienteResposta

5. **`POST /auth/criar_user`** ⚠️ REQUER TOKEN
   - Cria novo usuário (similar a registro)
   - Uso: Administrador criar usuários
   - Retorna: ClienteResposta

**Fluxo de Segurança:**
```
Entrada (email + senha)
    ↓
Valida: email único? CPF único? Senha válida?
    ↓
Criptografa senha com bcrypt
    ↓
Salva no banco
    ↓
Cria JWT token
    ↓
Retorna: Token + usuário
```

---

### 📦 **routers/prod_router.py** - PRODUTOS
**O que faz:** Define endpoints para CRUD de produtos.

**Endpoints:**

1. **`GET /produto/listar_produtos`** ✅ SEM autenticação
   - Lista todos os produtos
   - Público - qualquer um pode ver
   - Retorna: Lista de ProdutoResposta

2. **`GET /produto/produtos/{id}`** ✅ SEM autenticação
   - Obtém detalhes de um produto específico
   - Público - qualquer um pode ver
   - Retorna: ProdutoResposta

3. **`POST /produto/criar_produto`** ⚠️ REQUER TOKEN
   - Cria novo produto
   - Email extraído do token (para auditoria)
   - Retorna: ProdutoResposta com ID gerado

4. **`PUT /produto/atualizar_produto/{id}`** ⚠️ REQUER TOKEN
   - Atualiza produto existente
   - Permite atualização parcial
   - Retorna: ProdutoResposta atualizado

5. **`DELETE /produto/deletar_produto/{id}`** ⚠️ REQUER TOKEN
   - Deleta produto do catálogo
   - ⚠️ IRREVERSÍVEL!
   - Retorna: Mensagem de confirmação

**Segurança:**
- Endpoints de escrita (POST/PUT/DELETE) requerem autenticação
- Endpoints de leitura (GET) são públicos
- Email do usuário autenticado está disponível em cada endpoint protegido

---

### 🔧 **.env** - CONFIGURAÇÃO
**O que faz:** Armazena credenciais e configurações sensíveis (NÃO versionar!).

**Variáveis obrigatórias:**
```
DB_NAME=prova              # Nome do banco
DB_HOST=2dsmoca.tech       # Host do servidor MySQL
DB_USER=root               # Usuário MySQL
DB_PASSWORD=               # Senha MySQL
DB_PORT=3306               # Porta MySQL
SECRET_KEY=sua-chave-secreta  # Chave para assinar JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Tempo de expiração do token
```

**Segurança:**
- ⚠️ Nunca commit `.env` com credenciais reais em git
- ⚠️ Mude `SECRET_KEY` em produção para algo seguro e aleatório
- ✅ Use `.env.example` para documentar variáveis esperadas

---

### 📋 **requirements** - DEPENDÊNCIAS
**O que faz:** Lista todos os pacotes Python necessários.

**Principais pacotes instalados:**
```
fastapi==0.136.3           # Framework web
uvicorn==0.49.0            # Servidor ASGI
sqlalchemy==2.0.50         # ORM para banco de dados
pymysql==1.2.0             # Driver MySQL
pydantic==2.13.4           # Validação de dados
bcrypt==4.1.2              # Criptografia de senhas
passlib==1.7.4             # Gerenciador de hash
python-jose==3.3.0         # JWT (JSON Web Token)
pyjwt==2.8.1               # Alternativa JWT
python-dotenv==1.2.2       # Carrega .env
```

**Como instalar:**
```bash
pip install -r requirements
```

---

### 📚 **README.md** - DOCUMENTAÇÃO PRINCIPAL
**O que faz:** Documentação completa do projeto.

Contém:
- Visão geral das funcionalidades
- Como instalar e usar
- Exemplos de requisições
- Guia de segurança
- Troubleshooting
- Próximas melhorias sugeridas

---

### 🧪 **TESTES.md** - EXEMPLOS PRÁTICOS
**O que faz:** Exemplos de como testar a API com cURL.

Inclui:
- Passo a passo completo de testes
- Exemplos de sucesso e erro
- CURL commands prontos para copiar/colar
- Testes de segurança
- Fluxo completo

---

### ⚡ **REFERENCIA_RAPIDA.md** - CONSULTA RÁPIDA
**O que faz:** Resumo rápido para consulta durante desenvolvimento.

Inclui:
- Comandos essenciais
- O que cada coisa faz
- Tabelas do banco
- Fluxo de autenticação
- Erros comuns e soluções

---

### 📖 **GUIA_ARQUIVOS.md** - ESTE ARQUIVO
**O que faz:** Documentação completa de cada arquivo do projeto.

---

## 🔄 FLUXO COMPLETO DE UMA REQUISIÇÃO

### 1️⃣ Usuário registra
```
POST /auth/registro
    ↓
main.py → encontra router auth_router
    ↓
auth_router.registrar_usuario()
    ↓
Valida dados com ClienteRegistro (schemas.py)
    ↓
Criptografa senha: obter_hash_senha() (config.py)
    ↓
Salva em models.Cliente (models/model.py)
    ↓
Cria token: criar_access_token() (config.py)
    ↓
Retorna: Token + ClienteResposta
```

### 2️⃣ Usuário faz login
```
POST /auth/login
    ↓
auth_router.login_usuario()
    ↓
Valida Login schema
    ↓
Busca Cliente no banco
    ↓
Verifica senha: verificar_senha() (config.py)
    ↓
Cria token: criar_access_token() (config.py)
    ↓
Retorna: Token + ClienteResposta
```

### 3️⃣ Usuário acessa endpoint protegido
```
GET /auth/me com token no header
    ↓
FastAPI intercepta e verifica Depends(get_current_user_email)
    ↓
config.get_current_user_email() valida token
    ↓
Extrai email do token
    ↓
Retorna email para a função
    ↓
Função usa email para buscar dados
    ↓
Retorna ClienteResposta
```

### 4️⃣ Usuário cria produto
```
POST /produto/criar_produto com token
    ↓
prod_router.criar_produto() com Depends(get_current_user_email)
    ↓
Token é validado automaticamente
    ↓
Valida ProdutoBase schema
    ↓
Cria models.Produto
    ↓
Salva no banco
    ↓
Retorna ProdutoResposta com ID gerado
```

---

## 🎯 RESUMO: COMECE DAQUI

1. **main.py** ← Comece entendendo a estrutura básica
2. **config.py** ← Depois entenda segurança (JWT + bcrypt)
3. **schemas.py** ← Depois validação de dados
4. **models/model.py** ← Depois banco de dados
5. **routers/auth_router.py** ← Depois autenticação
6. **routers/prod_router.py** ← Por último produtos

---

**Todos os arquivos têm comentários! Leia o código! 📖**
