from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])

@router.get('/listar_usuario')
async def listar_user():
    return {'mensagem' : 'Lista de Usuarios'}