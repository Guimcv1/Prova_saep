from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ============= CONFIGURAÇÃO JWT =============
# Carrega a chave secreta do arquivo .env para assinar tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura-mude-em-producao")
# Define o algoritmo de criptografia usado para assinar tokens (HS256 = HMAC SHA-256)
ALGORITHM = "HS256"
# Define o tempo de expiração do token em minutos (30 minutos = token expira em 30 min)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============= CONFIGURAÇÃO CRIPTOGRAFIA =============
# Cria um contexto de criptografia usando bcrypt para hash de senhas
# bcrypt é mais seguro que outros métodos pois é mais lento para forçar ataque (brute force)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============= SEGURANÇA HTTP =============
# HTTPBearer é um esquema de segurança que extrai o token do header Authorization: Bearer <token>
security = HTTPBearer()

# ============= FUNÇÕES DE CRIPTOGRAFIA =============

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha plana corresponde ao hash armazenado.
    Utiliza bcrypt para comparação segura (não pode ser revertida).
    
    Args:
        senha_plana: A senha digitada pelo usuário
        senha_hash: O hash da senha armazenado no banco de dados
    
    Returns:
        bool: True se a senha é válida, False caso contrário
    """
    return pwd_context.verify(senha_plana, senha_hash)

def obter_hash_senha(senha: str) -> str:
    """
    Cria um hash bcrypt da senha para armazenamento seguro no banco.
    O hash é único a cada execução (inclui salt aleatório).
    
    Args:
        senha: A senha em texto plano do usuário
    
    Returns:
        str: O hash bcrypt da senha (nunca pode ser revertido)
    """
    return pwd_context.hash(senha)

# ============= FUNÇÕES JWT =============

def criar_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um token JWT (JSON Web Token) com os dados fornecidos.
    O token é assinado com a SECRET_KEY e inclui data de expiração.
    
    Args:
        data: Dicionário com dados a incluir no token (ex: {"sub": "email@example.com"})
        expires_delta: Tempo de expiração customizado (se None, usa ACCESS_TOKEN_EXPIRE_MINUTES)
    
    Returns:
        str: Token JWT codificado pronto para ser enviado ao cliente
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Adiciona a data de expiração ao token
    to_encode.update({"exp": expire})
    # Codifica e assina o token com a SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(credentials: HTTPAuthCredentials = Depends(security)):
    """
    Verifica se o token JWT fornecido é válido e não expirou.
    Extrai e valida o token do header Authorization.
    
    Args:
        credentials: Credenciais HTTP com Bearer token
    
    Returns:
        str: O email (subject) extraído do token válido
    
    Raises:
        HTTPException: Se o token for inválido ou expirado
    """
    token = credentials.credentials
    try:
        # Decodifica e valida o token usando a SECRET_KEY
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_email(credentials: HTTPAuthCredentials = Depends(security)):
    """
    Dependency (injeção de dependência) para obter o email do usuário autenticado.
    Use esta função em qualquer endpoint que necessite de autenticação.
    
    Exemplo de uso:
        @router.get("/me")
        async def meu_perfil(email: str = Depends(get_current_user_email)):
            return {"email": email}
    
    Args:
        credentials: Credenciais HTTP extraídas automaticamente do header
    
    Returns:
        str: O email do usuário autenticado
    """
    return verificar_token(credentials)
