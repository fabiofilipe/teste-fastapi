"""Router para gerenciamento de produtos do cardápio"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Produto, Usuario
from app.schemas.schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.dependencies import obter_usuario_admin
from app.exceptions import ProdutoJaExiste, ProdutoNaoEncontrado


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Cria um novo produto no cardápio"""
    # Verificar se já existe produto com mesmo nome e tamanho
    produto_existente = db.query(Produto).filter(
        Produto.nome == produto.nome,
        Produto.tamanho == produto.tamanho
    ).first()

    if produto_existente:
        raise ProdutoJaExiste(produto.nome, produto.tamanho)

    # Criar novo produto
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        categoria=produto.categoria,
        tamanho=produto.tamanho,
        preco=produto.preco,
        disponivel=produto.disponivel
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    disponivel: bool = None,
    categoria: str = None,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos do cardápio com filtros opcionais"""
    query = db.query(Produto)

    # Aplicar filtros se fornecidos
    if disponivel is not None:
        query = query.filter(Produto.disponivel == disponivel)

    if categoria:
        query = query.filter(Produto.categoria == categoria.upper())

    produtos = query.all()
    return produtos


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    """Busca um produto específico por ID"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Atualiza um produto existente"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    # Atualizar apenas campos fornecidos
    update_data = produto_update.model_dump(exclude_unset=True)

    for campo, valor in update_data.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Remove um produto do cardápio"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    db.delete(produto)
    db.commit()

    return None


@router.patch("/{produto_id}/disponibilidade", response_model=ProdutoResponse)
def alternar_disponibilidade(
    produto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Alterna a disponibilidade de um produto"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise ProdutoNaoEncontrado(produto_id)

    produto.disponivel = not produto.disponivel
    db.commit()
    db.refresh(produto)

    return produto
