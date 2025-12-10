"""Router para gerenciamento de categorias"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Categoria, Usuario
from app.schemas.schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.dependencies.auth import obter_usuario_admin
from app.exceptions import CategoriaNaoEncontrada, CategoriaJaExiste


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Cria uma nova categoria (apenas admin)"""
    # Verificar se categoria com mesmo nome ja existe
    existente = db.query(Categoria).filter(Categoria.nome == categoria.nome).first()
    if existente:
        raise CategoriaJaExiste(categoria.nome)

    nova_categoria = Categoria(**categoria.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(
    apenas_ativas: bool = True,
    db: Session = Depends(get_db)
):
    """Lista todas as categorias (filtro por ativas)"""
    query = db.query(Categoria)
    if apenas_ativas:
        query = query.filter(Categoria.ativa == True)
    categorias = query.order_by(Categoria.ordem_exibicao).all()
    return categorias


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def buscar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Busca categoria por ID"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise CategoriaNaoEncontrada(categoria_id)
    return categoria


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def atualizar_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Atualiza categoria (apenas admin)"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise CategoriaNaoEncontrada(categoria_id)

    update_data = categoria_update.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Deleta categoria (apenas admin)"""
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise CategoriaNaoEncontrada(categoria_id)

    db.delete(categoria)
    db.commit()
    return None
