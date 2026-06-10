from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, create_engine, DateTime
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# ============= CONFIGURAÇÃO DO BANCO DE DADOS =============

# Lê as variáveis de ambiente para conexão com o banco
db_name = os.getenv("DB_NAME")  # Nome do banco de dados
db_user = os.getenv("DB_USER",)  # Usuário do MySQL
db_password = os.getenv("DB_PASSWORD")  # Senha do MySQL
db_host = os.getenv("DB_HOST",'localhost')  # Host/IP do servidor MySQL
db_port = os.getenv('DB_PORT','3306')  # Porta do MySQL (padrão 3306)

# Constrói a URL de conexão no formato: mysql+pymysql://user:password@host:port/database
# pymysql = driver Python para MySQL
URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Cria engine (gerenciador de conexão com o banco)
# echo=True = imprime todas as queries SQL no console (útil para debug)
engine = create_engine(URL, echo=True)

# ============= BASE PARA MODELS =============

class Base(DeclarativeBase):
    """
    Classe base para todos os models SQLAlchemy.
    Todos os models devem herdar desta classe.
    """
    pass

# ============= MODELS =============

class Produto(Base):
    """
    Model para tabela 'Produto'.
    Representa produtos disponíveis no catálogo.
    """
    __tablename__ = "Produto"

    # ID único do produto (chave primária, auto incremento)
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    # Nome do produto (máximo 150 caracteres)
    nome = Column('nome', String(150))
    # Preço do produto (número decimal)
    preco = Column('preco', Float)
    # Data de validade do produto
    validade = Column('validade', String(10))

class Cliente(Base):
    """
    Model para tabela 'Cliente'.
    Representa usuários/clientes registrados no sistema.
    """
    __tablename__ = 'Cliente'

    # ID único do cliente (chave primária, auto incremento)
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    # Nome do cliente (máximo 150 caracteres, obrigatório)
    nome = Column('nome', String(150), nullable=False)
    # Email do cliente (único, obrigatório) - usado para login
    email = Column('email', String(150), nullable=False, unique=True)
    # Telefone do cliente (máximo 15 caracteres, obrigatório)
    telefone = Column('telefone', String(15), nullable=False)
    # CPF do cliente (único, obrigatório) - identificação brasileira
    cpf = Column('cpf', String(14), nullable=False, unique=True)
    # Hash bcrypt da senha (NUNCA armazenar senha em texto plano!)
    # Máximo 255 caracteres para acomodar o hash bcrypt
    senha_hash = Column('senha_hash', String(255), nullable=False)
    # Status VIP do cliente (True/False) - padrão é False
    vip = Column('vip', Boolean, default=False)

class Registro(Base):
    """
    Model para tabela 'Registro'.
    Representa transações/registros de vendas entre clientes e produtos.
    """
    __tablename__ = 'Registro'

    # ID único do registro (chave primária, auto incremento)
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    # ID do cliente envolvido na transação (chave estrangeira)
    # Referencia: Cliente.id
    cliente_id = Column('cliente_id', Integer, ForeignKey('Cliente.id'))
    # ID do produto envolvido na transação (chave estrangeira)
    # Referencia: Produto.id
    produto_id = Column('produto_id', Integer, ForeignKey('Produto.id'))
    # Data e hora do registro da transação
    data = Column('data', DateTime)
