# 🏗️ ESTRUTURA VISUAL DO PROJETO

## 📁 Árvore de Arquivos

```
Prova_saep/
│
├── 📄 main.py
│   └── Cria a app FastAPI
│       ├── Inclui auth_router
│       └── Inclui prod_router
│
├── 🔐 config.py
│   ├── obter_hash_senha() → bcrypt
│   ├── verificar_senha() → bcrypt
│   ├── criar_access_token() → JWT
│   ├── verificar_token() → JWT
│   └── get_current_user_email() → Dependency
│
├── ✅ schemas.py
│   ├── Cliente
│   │   ├── ClienteBase
│   │   ├── ClienteRegistro
│   │   ├── ClienteResposta
│   │   └── ClienteAtualizar
│   ├── Autenticação
│   │   ├── Login
│   │   ├── Token
│   │   └── TokenData
│   ├── Produto
│   │   ├── ProdutoBase
│   │   ├── ProdutoResposta
│   │   └── ProdutoAtualizar
│   └── Registro
│       ├── RegistroBase
│       └── RegistroResposta
│
├── 💾 models/
│   └── model.py
│       ├── Cliente (table)
│       │   ├── id (PK)
│       │   ├── nome
│       │   ├── email (UNIQUE)
│       │   ├── telefone
│       │   ├── cpf (UNIQUE)
│       │   ├── senha_hash
│       │   └── vip
│       ├── Produto (table)
│       │   ├── id (PK)
│       │   ├── nome
│       │   ├── preco
│       │   └── validade
│       └── Registro (table)
│           ├── id (PK)
│           ├── cliente_id (FK)
│           ├── produto_id (FK)
│           └── data
│
├── 🛣️ routers/
│   ├── auth_router.py
│   │   ├── POST /auth/registro (sem token)
│   │   ├── POST /auth/login (sem token)
│   │   ├── GET /auth/me (com token)
│   │   ├── GET /auth/listar_usuario (com token)
│   │   └── POST /auth/criar_user (com token)
│   │
│   └── prod_router.py
│       ├── GET /produto/listar_produtos (sem token)
│       ├── GET /produto/produtos/{id} (sem token)
│       ├── POST /produto/criar_produto (com token)
│       ├── PUT /produto/atualizar_produto/{id} (com token)
│       └── DELETE /produto/deletar_produto/{id} (com token)
│
├── 🔧 .env
│   ├── DB_NAME
│   ├── DB_HOST
│   ├── DB_USER
│   ├── DB_PASSWORD
│   ├── DB_PORT
│   ├── SECRET_KEY
│   └── ACCESS_TOKEN_EXPIRE_MINUTES
│
├── 📋 requirements
│   ├── fastapi
│   ├── uvicorn
│   ├── sqlalchemy
│   ├── pymysql
│   ├── pydantic
│   ├── bcrypt
│   ├── passlib
│   ├── python-jose
│   ├── pyjwt
│   └── python-dotenv
│
├── 📚 Documentação
│   ├── README.md
│   ├── TESTES.md
│   ├── REFERENCIA_RAPIDA.md
│   ├── GUIA_ARQUIVOS.md
│   ├── CHECKLIST.md
│   ├── ESTRUTURA_VISUAL.md (este arquivo)
│   └── alembic.ini (migrações)
│
└── 🗂️ alembic/
    ├── env.py
    ├── script.py.mako
    └── README
```

---

## 🔄 FLUXO DE DADOS - ARQUITETURA

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENTE/FRONTEND                        │
│                  (Postman, cURL, Browser)                    │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI (main.py)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Routers                                             │   │
│  │ ├── auth_router.py      ← endpoints /auth/*        │   │
│  │ └── prod_router.py      ← endpoints /produto/*     │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌────────────┐  ┌────────────┐  ┌──────────┐
    │ Validação  │  │ Segurança  │  │ Lógica   │
    │ (Pydantic) │  │ (JWT/bcrypt│  │ Business │
    │ schemas.py │  │ config.py) │  │ models   │
    └────────────┘  └────────────┘  └──────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
         ┌─────────────────────────────┐
         │  SQLAlchemy ORM (models/)   │
         │  ├── Cliente table          │
         │  ├── Produto table          │
         │  └── Registro table         │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │   MySQL Database            │
         │  (2dsmoca.tech:3306)        │
         │  ├── Cliente                │
         │  ├── Produto                │
         │  └── Registro               │
         └─────────────────────────────┘
```

---

## 🔐 FLUXO DE SEGURANÇA

```
REGISTRO/LOGIN
───────────────────────────────────────────────
Usuário: email + senha (texto plano)
         │
         ▼
    ┌─────────────────────────┐
    │  Validação Pydantic     │
    │  - Email válido?        │
    │  - Senha ≥ 8 chars?     │
    │  - Formato correto?     │
    └────────────┬────────────┘
                 │
                 ▼ (válido)
         ┌───────────────┐
         │  Bcrypt Hash  │ (config.py)
         │  +salt aleat. │
         └───────┬───────┘
                 │
                 ▼ (hash irreversível)
         ┌──────────────────┐
         │  Salva no banco  │
         │  (NUNCA texto!)  │
         └─────────┬────────┘
                   │
                   ▼
         ┌──────────────────┐
         │  Cria JWT Token  │ (config.py)
         │  - Secret Key    │
         │  - HS256         │
         │  - Exp 30 min    │
         └─────────┬────────┘
                   │
                   ▼
         ┌──────────────────┐
         │ Retorna Token    │
         │ + dados usuário  │
         └──────────────────┘

PRÓXIMAS REQUISIÇÕES
───────────────────────────────────────────────
Cliente: Authorization: Bearer <token>
         │
         ▼
    ┌─────────────────────┐
    │  Dependency Injection│
    │  HTTPBearer()       │
    └──────────┬──────────┘
               │
               ▼
    ┌─────────────────────┐
    │  JWT Decode         │
    │  - Valida Secret Key│
    │  - Verifica exp?    │
    │  - Extrai email     │
    └──────────┬──────────┘
               │
         ┌─────┴─────┐
         ▼           ▼
    ✅ Válido   ❌ Inválido
         │           │
         ▼           ▼
    Email para    Erro 401
    função      Unauthorized
```

---

## 🌐 ENDPOINTS - MAPA VISUAL

```
BASE: http://localhost:8000

AUTENTICAÇÃO (SEM TOKEN NECESSÁRIO)
│
├── POST /auth/registro
│   └─ Input: nome, email, telefone, cpf, senha
│   └─ Output: token + usuário
│   └─ Valida: email único, cpf único, senha ≥ 8 chars
│
└── POST /auth/login
    └─ Input: email, senha
    └─ Output: token + usuário
    └─ Valida: credenciais corretas


AUTENTICAÇÃO (REQUER TOKEN)
│
├── GET /auth/me
│   └─ Output: dados do usuário autenticado
│   └─ Email extraído do token
│
├── GET /auth/listar_usuario
│   └─ Output: lista de todos os usuários
│
└── POST /auth/criar_user
    └─ Input: nome, email, telefone, cpf, senha
    └─ Output: novo usuário criado
    └─ Uso: Administrador


PRODUTOS (SEM TOKEN - LEITURA)
│
├── GET /produto/listar_produtos
│   └─ Output: lista de todos os produtos
│   └─ Público!
│
└── GET /produto/produtos/{id}
    └─ Output: detalhes do produto
    └─ Público!


PRODUTOS (REQUER TOKEN - ESCRITA)
│
├── POST /produto/criar_produto
│   └─ Input: nome, preco, validade
│   └─ Output: produto com ID gerado
│
├── PUT /produto/atualizar_produto/{id}
│   └─ Input: nome?, preco?, validade? (opcionais)
│   └─ Output: produto atualizado
│   └─ Atualização parcial!
│
└── DELETE /produto/deletar_produto/{id}
    └─ Output: mensagem de sucesso
    └─ IRREVERSÍVEL!


DOCUMENTAÇÃO
│
├── GET /docs
│   └─ Swagger UI (recomendado!)
│
├── GET /redoc
│   └─ ReDoc UI
│
└── GET /
    └─ Info sobre API
```

---

## 🔌 SEQUÊNCIA DE REQUISIÇÃO

```
1. REGISTRO
   ┌────────────────────────────────────┐
   │ Client                             │
   │ POST /auth/registro                │
   │ {nome, email, telefone, cpf,senha}│
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ FastAPI + Pydantic Validation      │
   │ - Valida tipos                     │
   │ - Valida email format              │
   │ - Valida comprimentos              │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ auth_router.registrar_usuario()    │
   │ - Verifica email único             │
   │ - Verifica cpf único               │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ config.obter_hash_senha()          │
   │ - Bcrypt(senha + salt aleatório)   │
   │ - Retorna hash irreversível        │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ models.Cliente INSERT              │
   │ - Salva: nome, email, cpf          │
   │ - Salva: senha_hash (não senha!)   │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ config.criar_access_token()        │
   │ - JWT com SECRET_KEY               │
   │ - Exp 30 min                       │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ Client recebe resposta             │
   │ {access_token, token_type, user}   │
   └────────────────────────────────────┘


2. LOGIN
   ┌────────────────────────────────────┐
   │ Client                             │
   │ POST /auth/login                   │
   │ {email, senha}                     │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ auth_router.login_usuario()        │
   │ - Busca Cliente por email          │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ config.verificar_senha()           │
   │ - Bcrypt compara:                  │
   │   senha_digitada vs hash_banco     │
   └─────────────────┬──────────────────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
           ✅ OK        ❌ ERRO
              │             │
              ▼             ▼
         Cria token    Erro 401
              │
              ▼
   ┌────────────────────────────────────┐
   │ Client recebe token + user         │
   └────────────────────────────────────┘


3. ACESSAR ENDPOINT PROTEGIDO
   ┌────────────────────────────────────┐
   │ Client                             │
   │ GET /auth/me                       │
   │ Header: Authorization: Bearer xxx  │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ FastAPI Dependency                 │
   │ Depends(get_current_user_email)    │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ config.get_current_user_email()    │
   │ - Extrai token do header           │
   │ - Decodifica JWT                   │
   │ - Valida assinatura                │
   │ - Verifica expiração               │
   └─────────────────┬──────────────────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
           ✅ OK        ❌ ERRO
              │             │
              ▼             ▼
         Extrai email   Erro 401
              │
              ▼
   ┌────────────────────────────────────┐
   │ obter_usuario_atual(email)         │
   │ - Busca Cliente por email          │
   └─────────────────┬──────────────────┘
                     │
                     ▼
   ┌────────────────────────────────────┐
   │ Client recebe dados do usuário     │
   │ {id, nome, email, ...}             │
   │ (SEM senha!)                       │
   └────────────────────────────────────┘
```

---

## 📊 DIAGRAMA DE ENTIDADES

```
┌──────────────────────────────┐
│         CLIENTE              │
├──────────────────────────────┤
│ id (PK)                      │
│ nome (String 150)            │
│ email (String 150, UNIQUE)   │
│ telefone (String 15)         │
│ cpf (String 14, UNIQUE)      │
│ senha_hash (String 255)      │
│ vip (Boolean)                │
└──────────────────────────────┘
         │
         │ 1:N
         │
         ▼
┌──────────────────────────────┐
│        REGISTRO              │
├──────────────────────────────┤
│ id (PK)                      │
│ cliente_id (FK)  ─────────┐  │
│ produto_id (FK)  ──────┐  │  │
│ data (DateTime)        │  │  │
└──────────────────────────────┘
                         │
         ┌───────────────┘
         │
         ▼
┌──────────────────────────────┐
│        PRODUTO               │
├──────────────────────────────┤
│ id (PK)                      │
│ nome (String 150)            │
│ preco (Float)                │
│ validade (String 10)         │
└──────────────────────────────┘
```

---

## 🎯 MAPA DE DEPENDÊNCIAS

```
main.py
├── from routers.auth_router import router as auth_router
│   ├── from models.model import Cliente
│   ├── from schemas import ClienteRegistro, ClienteResposta, Login, Token
│   └── from config import obter_hash_senha, verificar_senha, criar_access_token, get_current_user_email
│       ├── from passlib.context import CryptContext (bcrypt)
│       ├── from jose import JWTError, jwt (JWT)
│       └── from dotenv import load_dotenv (carrega .env)
│
├── from routers.prod_router import router as prod_router
│   ├── from models.model import Produto
│   ├── from schemas import ProdutoBase, ProdutoResposta, ProdutoAtualizar
│   └── from config import get_current_user_email
│
└── Executa em:
    uvicorn main:app --reload
```

---

## ✨ SUMÁRIO VISUAL

```
┌─ CAMADA DE APRESENTAÇÃO
│  └─ FastAPI/HTTP REST API
│     ├─ /auth/* (autenticação)
│     └─ /produto/* (produtos)
│
├─ CAMADA DE NEGÓCIO
│  ├─ Validação (Pydantic schemas.py)
│  ├─ Segurança (config.py - JWT + bcrypt)
│  └─ Lógica (routers/)
│
├─ CAMADA DE DADOS
│  ├─ ORM (SQLAlchemy models/)
│  └─ Banco MySQL (3 tabelas)
│
└─ CONFIGURAÇÃO
   ├─ .env (variáveis de ambiente)
   └── requirements (dependências)

SEGURANÇA EM CAMADAS:
1. Validação de entrada (Pydantic)
2. Criptografia de senha (Bcrypt)
3. Autenticação JWT (HMAC-SHA256)
4. Proteção de endpoints (Dependency Injection)
```

---

**ESTRUTURA PRONTA E DOCUMENTADA! 📚**
