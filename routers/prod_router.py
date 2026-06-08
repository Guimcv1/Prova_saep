from fastapi import APIRouter

router = APIRouter(prefix='/produto', tags=['produto'])

@router.get('/listar_produtos')
async def listar_produtos():
    return {'mensagem' : 'Lista de produtos'}