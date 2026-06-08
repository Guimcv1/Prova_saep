from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean,create_engine, DateTime
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER",)
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST",'localhost')
db_port = os.getenv('DB_PORT','3306')

URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(URL,echo=True)

class Base(DeclarativeBase):
    pass

class Produto(Base):
    __tablename__ = "Produto"

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column('nome', String(150))
    preco = Column('preco', Float)
    validade = Column('validade', String(10))

class Cliente(Base):
    __tablename__ = 'Cliente'

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column('nome', String(150))
    telefone = Column('telefone', Integer)
    cpf = Column('cpf', Integer)
    vip = Column('vip', Boolean)

class Registro(Base):
    __tablename__ = 'Registro'

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    cliente_id = Column('cliente_id', ForeignKey(Cliente.id))
    produto_id = Column('produto_id', ForeignKey(Produto.id))
    data = Column('data',DateTime)

Base.metadata.create_all(engine)