# ============= IMPORTAÇÕES =============
from fastapi import FastAPI
from routers.auth_router import router as auth_router
from routers.prod_router import router as prod_router

# ============= CRIAÇÃO DA APLICAÇÃO =============
# Cria a aplicação FastAPI
# title = nome da API (aparece na documentação)
# description = descrição da API (aparece na documentação)
app = FastAPI(
    title="Prova SAEP API",
    description="API com autenticação JWT, criptografia de senhas e gestão de clientes e produtos"
)

# ============= INCLUSÃO DOS ROUTERS =============
# Inclui os routers na aplicação principal
# Isso registra todos os endpoints dos routers

# Router de autenticação (endpoints /auth/*)
# Contém: registro, login, obter usuário, listar usuários, etc.
app.include_router(auth_router)

# Router de produtos (endpoints /produto/*)
# Contém: listar, criar, atualizar, deletar produtos, etc.
app.include_router(prod_router)

# ============= ENDPOINT RAIZ (opcional) =============

@app.get("/")
async def root():
    """
    Endpoint raiz - retorna informações sobre a API.
    
    Acesse http://localhost:8000/docs para documentação interativa (Swagger).
    """
    return {
        "mensagem": "Bem-vindo à Prova SAEP API",
        "versao": "1.0.0",
        "endpoints": {
            "documentacao_swagger": "/docs",
            "documentacao_redoc": "/redoc",
            "autenticacao": "/auth/*",
            "produtos": "/produto/*"
        }
    }

# ============= COMO EXECUTAR =============
# No terminal, execute: uvicorn main:app --reload
# A API estará disponível em http://localhost:8000


