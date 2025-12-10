"""Router publico para visualizacao do cardapio"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.database import get_db
from app.models.models import Categoria, Produto, ProdutoIngrediente
from app.schemas.schemas import CardapioResponse, CardapioCategoria, ProdutoResponse


router = APIRouter(
    prefix="/cardapio",
    tags=["Cardapio"]
)


@router.get("/", response_model=CardapioResponse)
def listar_cardapio_completo(
    db: Session = Depends(get_db)
):
    """
    Lista cardapio completo com categorias ativas e produtos disponiveis

    Retorna categorias ordenadas por ordem_exibicao, com produtos aninhados
    """
    # Carregar categorias com produtos, variacoes e ingredientes em uma unica query
    categorias = db.query(Categoria)\
        .options(
            joinedload(Categoria.produtos)
            .joinedload(Produto.variacoes)
        )\
        .options(
            joinedload(Categoria.produtos)
            .joinedload(Produto.ingredientes)
            .joinedload(ProdutoIngrediente.ingrediente)
        )\
        .filter(Categoria.ativa == True)\
        .order_by(Categoria.ordem_exibicao)\
        .all()

    # Filtrar apenas produtos disponiveis
    cardapio_data = []
    for categoria in categorias:
        produtos_disponiveis = [p for p in categoria.produtos if p.disponivel and not p.deleted_at]
        if produtos_disponiveis:  # Apenas incluir categoria se tiver produtos disponiveis
            cardapio_data.append({
                "id": categoria.id,
                "nome": categoria.nome,
                "descricao": categoria.descricao,
                "icone": categoria.icone,
                "ordem_exibicao": categoria.ordem_exibicao,
                "produtos": produtos_disponiveis
            })

    return {"categorias": cardapio_data}


@router.get("/categorias/{categoria_id}/produtos", response_model=List[ProdutoResponse])
def listar_produtos_por_categoria(
    categoria_id: int,
    incluir_indisponiveis: bool = False,
    db: Session = Depends(get_db)
):
    """
    Lista produtos de uma categoria especifica

    - **categoria_id**: ID da categoria
    - **incluir_indisponiveis**: Se True, inclui produtos indisponiveis
    """
    query = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(Produto.categoria_id == categoria_id)

    if not incluir_indisponiveis:
        query = query.filter(Produto.disponivel == True)

    produtos = query.all()
    return produtos


@router.get("/buscar", response_model=List[ProdutoResponse])
def buscar_produtos(
    termo: str = Query(..., min_length=2, description="Termo de busca"),
    db: Session = Depends(get_db)
):
    """
    Busca produtos por nome ou descricao

    - **termo**: Termo de busca (minimo 2 caracteres)
    """
    produtos = db.query(Produto)\
        .options(joinedload(Produto.variacoes))\
        .options(joinedload(Produto.ingredientes).joinedload(ProdutoIngrediente.ingrediente))\
        .filter(
            Produto.disponivel == True,
            (Produto.nome.ilike(f"%{termo}%") | Produto.descricao.ilike(f"%{termo}%"))
        )\
        .all()

    return produtos
