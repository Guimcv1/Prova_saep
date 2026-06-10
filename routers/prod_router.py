from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import sessionmaker
from models.model import engine, Produto, Cliente
from schemas import ProdutoBase, ProdutoResposta, ProdutoAtualizar, RegistroResposta
from config import get_current_user_email
from datetime import datetime

# Cria o roteador para endpoints de produtos
# prefix='/produto' = todos os endpoints começam com /produto
# tags=['produto'] = agrupa no Swagger documentation
router = APIRouter(prefix='/produto', tags=['produto'])

# Cria a sessão do banco de dados
SessionLocal = sessionmaker(bind=engine)

# ============= ENDPOINTS DE PRODUTOS =============

@router.get('/listar_produtos', response_model=list[ProdutoResposta])
async def listar_produtos():
    """
    Lista todos os produtos disponíveis no catálogo.
    
    ✅ NÃO requer autenticação - qualquer um pode ver produtos.
    
    Retorna uma lista de todos os produtos com seus dados (nome, preço, validade).
    """
    session = SessionLocal()
    try:
        # Busca todos os produtos do banco
        produtos = session.query(Produto).all()
        # Converte para response models
        return [ProdutoResposta.from_orm(produto) for produto in produtos]
    finally:
        session.close()

@router.get('/produtos/{produto_id}', response_model=ProdutoResposta)
async def obter_produto(produto_id: int):
    """
    Obtém informações detalhadas de um produto específico pelo ID.
    
    ✅ NÃO requer autenticação.
    
    Retorna os dados completos do produto (nome, preço, validade).
    """
    session = SessionLocal()
    try:
        # Busca o produto com o ID fornecido
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        
        # Se não encontrou, retorna erro 404
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        return ProdutoResposta.from_orm(produto)
    finally:
        session.close()

@router.post('/criar_produto', response_model=ProdutoResposta)
async def criar_produto(
    produto: ProdutoBase,
    email: str = Depends(get_current_user_email)
):
    """
    Cria um novo produto no catálogo.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    Apenas usuários autenticados podem adicionar novos produtos ao sistema.
    
    Retorna os dados do novo produto criado (com ID gerado automaticamente).
    """
    session = SessionLocal()
    try:
        # Cria novo objeto Produto com os dados fornecidos
        novo_produto = Produto(
            nome=produto.nome,
            preco=produto.preco,
            validade=produto.validade
        )
        
        # Adiciona à sessão e salva no banco
        session.add(novo_produto)
        session.commit()
        session.refresh(novo_produto)  # Recarrega para obter o ID gerado
        
        return ProdutoResposta.from_orm(novo_produto)
    
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar produto: {str(e)}"
        )
    finally:
        session.close()

@router.put('/atualizar_produto/{produto_id}', response_model=ProdutoResposta)
async def atualizar_produto(
    produto_id: int,
    produto_atualizado: ProdutoAtualizar,
    email: str = Depends(get_current_user_email)
):
    """
    Atualiza os dados de um produto existente.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    Permite atualização parcial: você pode atualizar apenas alguns campos.
    Os campos não fornecidos mantêm seus valores originais.
    
    Retorna os dados atualizados do produto.
    """
    session = SessionLocal()
    try:
        # Busca o produto que será atualizado
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        
        # Se não encontrou, retorna erro 404
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        # Atualiza apenas os campos que foram fornecidos (não None)
        if produto_atualizado.nome is not None:
            produto.nome = produto_atualizado.nome
        if produto_atualizado.preco is not None:
            produto.preco = produto_atualizado.preco
        if produto_atualizado.validade is not None:
            produto.validade = produto_atualizado.validade
        
        # Salva as alterações no banco
        session.commit()
        session.refresh(produto)
        
        return ProdutoResposta.from_orm(produto)
    
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )
    finally:
        session.close()

@router.delete('/deletar_produto/{produto_id}')
async def deletar_produto(
    produto_id: int,
    email: str = Depends(get_current_user_email)
):
    """
    Deleta um produto do catálogo.
    
    ⚠️ REQUER AUTENTICAÇÃO: Deve enviar token JWT no header Authorization: Bearer <token>
    
    Remove permanentemente o produto do banco de dados.
    ⚠️ CUIDADO: Esta operação não pode ser desfeita!
    
    Retorna mensagem de confirmação.
    """
    session = SessionLocal()
    try:
        # Busca o produto que será deletado
        produto = session.query(Produto).filter(Produto.id == produto_id).first()
        
        # Se não encontrou, retorna erro 404
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        
        # Remove o produto do banco de dados
        session.delete(produto)
        session.commit()
        
        return {"mensagem": "Produto deletado com sucesso"}
    
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )
    finally:
        session.close()