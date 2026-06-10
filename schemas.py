from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= CLIENTE SCHEMAS =============

class ClienteBase(BaseModel):
    """
    Schema base para Cliente com campos comuns.
    Utilizado como base para outros schemas de cliente.
    """
    nome: str = Field(..., min_length=1, max_length=150, description="Nome do cliente")
    email: EmailStr = Field(..., description="Email do cliente (validado automaticamente)")
    telefone: str = Field(..., min_length=10, max_length=15, description="Telefone do cliente")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do cliente")

class ClienteRegistro(ClienteBase):
    """
    Schema para registro de novo cliente.
    Inclui a senha que será criptografada no servidor.
    Herda nome, email, telefone e cpf do ClienteBase.
    """
    senha: str = Field(..., min_length=8, description="Senha com no mínimo 8 caracteres")

class ClienteResposta(ClienteBase):
    """
    Schema para resposta de dados do cliente.
    Retorna os dados do cliente EXCETO a senha (por segurança).
    Inclui o ID e status VIP do cliente.
    Utilizado em endpoints GET, resposta de login/registro, etc.
    """
    id: int
    vip: bool = False
    
    class Config:
        # Permite converter objetos SQLAlchemy diretamente em Pydantic models
        from_attributes = True

class ClienteAtualizar(BaseModel):
    """
    Schema para atualização parcial de dados do cliente.
    Todos os campos são opcionais (pode atualizar apenas alguns).
    """
    nome: Optional[str] = Field(None, max_length=150)
    telefone: Optional[str] = Field(None, min_length=10, max_length=15)

# ============= AUTENTICAÇÃO SCHEMAS =============

class Login(BaseModel):
    """
    Schema para credenciais de login.
    Usado no endpoint POST /auth/login
    """
    email: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha do usuário")

class Token(BaseModel):
    """
    Schema para resposta de token após login/registro.
    Contém o JWT token, tipo de token e dados do usuário.
    """
    access_token: str
    token_type: str = "bearer"
    usuario: ClienteResposta

class TokenData(BaseModel):
    """
    Schema para dados extraídos do token JWT.
    Utilizado internamente para verificação de tokens.
    """
    email: Optional[str] = None
    exp: Optional[datetime] = None

# ============= PRODUTO SCHEMAS =============

class ProdutoBase(BaseModel):
    """
    Schema base para Produto com campos obrigatórios.
    Utilizado como base para schemas de criação e atualização.
    """
    nome: str = Field(..., min_length=1, max_length=150, description="Nome do produto")
    preco: float = Field(..., gt=0, description="Preço do produto (deve ser maior que 0)")
    validade: str = Field(..., description="Data de validade (DD/MM/YYYY)")

class ProdutoResposta(ProdutoBase):
    """
    Schema para resposta de dados do produto.
    Retorna todos os dados do produto incluindo ID.
    Usado em endpoints GET e após criação/atualização.
    """
    id: int
    
    class Config:
        # Permite converter objetos SQLAlchemy diretamente em Pydantic models
        from_attributes = True

class ProdutoAtualizar(BaseModel):
    """
    Schema para atualização parcial de produto.
    Todos os campos são opcionais (pode atualizar apenas alguns).
    """
    nome: Optional[str] = Field(None, max_length=150)
    preco: Optional[float] = Field(None, gt=0)
    validade: Optional[str] = None

# ============= REGISTRO SCHEMAS =============

class RegistroBase(BaseModel):
    """
    Schema base para Registro de venda/transação.
    Contém IDs de cliente e produto envolvidos na transação.
    """
    cliente_id: int
    produto_id: int

class RegistroResposta(RegistroBase):
    """
    Schema para resposta de dados do registro.
    Retorna o registro com ID e data/hora da transação.
    Usado em endpoints GET após criação de registro.
    """
    id: int
    data: datetime
    
    class Config:
        # Permite converter objetos SQLAlchemy diretamente em Pydantic models
        from_attributes = True
