from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from models.model import engine

router = APIRouter(prefix='/auth', tags=['auth'])

@router.get('/listar_usuario')
async def listar_user():
    return {'mensagem' : 'Lista de Usuarios'}


@router.post('/criar_user')
async def criar_user(nome:str, telefone:int, cpf:int):
    sesion = sessionmaker(bind=engine)
    Sesion = sesion()
    email_verify = Sesion.query(Cliente).filter(Cliente.cpf==cpf).first()
    if email_verify:
        return {'Mensagem':'Usuario já existe'}
    novo_usuario = Cliente(nome, telefone, cpf, vip=False)
    Sesion.add(novo_usuario)
    Sesion.commit()
    return {"Mensagem":"Usuario criado com sucesso"}
