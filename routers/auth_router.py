from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from models.model import engine, Cliente
from schemas import ClienteRegistro, ClienteResposta, Login, Token
from config import obter_hash_senha, verificar_senha, criar_access_token, get_current_user_email
from datetime import timedelta

# Cria o roteador para endpoints de autenticação
# prefix='/auth' = todos os endpoints começam com /auth
# tags=['auth'] = agrupa no Swagger documentation
router = APIRouter(prefix='/auth', tags=['auth'])

# Cria a sessão do banco de dados
# Usar sessionmaker garante que cada requisição tenha sua própria sessão
SessionLocal = sessionmaker(bind=engine)

# ============= ENDPOINTS DE AUTENTICAÇÃO =============

@router.post('/registro', response_model=Token)
async def registrar_usuario(usuario: ClienteRegistro):
    """
    Registra um novo usuário no sistema.
    
    Processo:
    1. Verifica se o email já existe (deve ser único)
    2. Verifica se o CPF já existe (deve ser único)
    3. Criptografa a senha com bcrypt
    4. Cria novo registro no banco de dados
    5. Gera JWT token automaticamente
    
    Retorna o token JWT e dados do novo usuário.
    """
    session = SessionLocal()
    try:
        # Busca se já existe alguém com este email
        email_existente = session.query(Cliente).filter(Cliente.email == usuario.email).first()
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Busca se já existe alguém com este CPF
        cpf_existente = session.query(Cliente).filter(Cliente.cpf == usuario.cpf).first()
        if cpf_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )
        
        # Criptografa a senha (é irreversível e seguro)
        senha_hash = obter_hash_senha(usuario.senha)
        
        # Cria novo objeto Cliente com os dados fornecidos
        novo_cliente = Cliente(
            nome=usuario.nome,
            email=usuario.email,
            telefone=usuario.telefone,
            cpf=usuario.cpf,
            senha_hash=senha_hash,  # Armazena a senha criptografada, NUNCA em texto plano
            vip=False  # Novo usuário começa com vip=False
        )
        
        # Adiciona à sessão e confirma a transação (salva no banco)
        session.add(novo_cliente)
        session.commit()
        session.refresh(novo_cliente)  # Recarrega para obter o ID gerado
        
        # Cria JWT token válido por 30 minutos
        access_token = criar_access_token(
            data={"sub": novo_cliente.email},  # "sub" = subject (identificador do usuário)
            expires_delta=timedelta(minutes=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": ClienteResposta.from_orm(novo_cliente)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        # Se algo der errado, desfaz a transação (rollback)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao registrar usuário: {str(e)}"
        )
    finally:
        # Sempre fecha a sessão para liberar recursos
        session.close()

@router.post('/login', response_model=Token)
async def login_usuario(credenciais: Login):
    """
    Realiza login do usuário e retorna token JWT.
    
    Processo:
    1. Busca o usuário pelo email no banco
    2. Verifica se a senha está correta usando bcrypt
    3. Se válido, gera JWT token
    
    Retorna o token JWT e dados do usuário autenticado.
    """
    session = SessionLocal()
    try:
        # Busca o cliente com este email no banco de dados
        cliente = session.query(Cliente).filter(Cliente.email == credenciais.email).first()
        
        # Se não encontrou o email, retorna erro genérico (segurança)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verifica se a senha digitada corresponde ao hash armazenado
        # verificar_senha compara de forma segura (usa bcrypt)
        if not verificar_senha(credenciais.senha, cliente.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Se chegou aqui, as credenciais são válidas
        # Cria JWT token válido por 30 minutos
        access_token = criar_access_token(
            data={"sub": cliente.email},
            expires_delta=timedelta(minutes=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": ClienteResposta.from_orm(cliente)
        }
    
    finally:
        session.close()

# ============= ENDPOINTS PROTEGIDOS =============

@router.get('/me', response_model=ClienteResposta)
async def obter_usuario_atual(email: str = Depends(get_current_user_email)):
    """
    Retorna informações do usuário autenticado.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    O email é extraído e validado automaticamente do token JWT.
    Se o token for inválido ou expirado, retorna erro 401.
    """
    session = SessionLocal()
    try:
        # Busca o cliente usando o email extraído do token
        cliente = session.query(Cliente).filter(Cliente.email == email).first()
        
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return ClienteResposta.from_orm(cliente)
    finally:
        session.close()

@router.get('/listar_usuario', response_model=list[ClienteResposta])
async def listar_usuarios(email: str = Depends(get_current_user_email)):
    """
    Lista todos os usuários registrados no sistema.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    Retorna uma lista de todos os clientes sem as senhas (por segurança).
    """
    session = SessionLocal()
    try:
        # Busca todos os clientes no banco
        clientes = session.query(Cliente).all()
        # Converte para response models (sem senhas)
        return [ClienteResposta.from_orm(cliente) for cliente in clientes]
    finally:
        session.close()

@router.post('/criar_user', response_model=ClienteResposta)
async def criar_user_auth(
    usuario: ClienteRegistro,
    email_autenticado: str = Depends(get_current_user_email)
):
    """
    Cria novo usuário no sistema.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    Endpoint alternativo para criar usuário (similar a /registro mas requer autenticação).
    Útil quando um administrador quer criar usuários.
    
    Retorna os dados do novo usuário criado.
    """
    session = SessionLocal()
    try:
        # Verifica se o email já existe (deve ser único)
        email_existente = session.query(Cliente).filter(Cliente.email == usuario.email).first()
        if email_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Verifica se o CPF já existe (deve ser único)
        cpf_existente = session.query(Cliente).filter(Cliente.cpf == usuario.cpf).first()
        if cpf_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado"
            )
        
        # Criptografa a senha
        senha_hash = obter_hash_senha(usuario.senha)
        
        # Cria novo cliente
        novo_cliente = Cliente(
            nome=usuario.nome,
            email=usuario.email,
            telefone=usuario.telefone,
            cpf=usuario.cpf,
            senha_hash=senha_hash,
            vip=False
        )
        
        session.add(novo_cliente)
        session.commit()
        session.refresh(novo_cliente)
        
        return ClienteResposta.from_orm(novo_cliente)
    
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )
    finally:
        session.close()
