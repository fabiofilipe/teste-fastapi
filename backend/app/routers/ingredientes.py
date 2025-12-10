"""Router para gerenciamento de ingredientes"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Ingrediente, Usuario
from app.schemas.schemas import IngredienteCreate, IngredienteUpdate, IngredienteResponse
from app.dependencies.auth import obter_usuario_admin
from app.exceptions import IngredienteNaoEncontrado


router = APIRouter(
    prefix="/ingredientes",
    tags=["Ingredientes"]
)


@router.post("/", response_model=IngredienteResponse, status_code=status.HTTP_201_CREATED)
def criar_ingrediente(
    ingrediente: IngredienteCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Cria novo ingrediente (apenas admin)"""
    novo_ingrediente = Ingrediente(**ingrediente.model_dump())
    db.add(novo_ingrediente)
    db.commit()
    db.refresh(novo_ingrediente)
    return novo_ingrediente


@router.get("/", response_model=List[IngredienteResponse])
def listar_ingredientes(
    apenas_disponiveis: bool = False,
    db: Session = Depends(get_db)
):
    """Lista todos os ingredientes"""
    query = db.query(Ingrediente)
    if apenas_disponiveis:
        query = query.filter(Ingrediente.disponivel == True)
    ingredientes = query.order_by(Ingrediente.nome).all()
    return ingredientes


@router.get("/{ingrediente_id}", response_model=IngredienteResponse)
def buscar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    """Busca ingrediente por ID"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise IngredienteNaoEncontrado(ingrediente_id)
    return ingrediente


@router.put("/{ingrediente_id}", response_model=IngredienteResponse)
def atualizar_ingrediente(
    ingrediente_id: int,
    ingrediente_update: IngredienteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Atualiza ingrediente (apenas admin)"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise IngredienteNaoEncontrado(ingrediente_id)

    update_data = ingrediente_update.model_dump(exclude_unset=True)
    for campo, valor in update_data.items():
        setattr(ingrediente, campo, valor)

    db.commit()
    db.refresh(ingrediente)
    return ingrediente


@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Deleta ingrediente (apenas admin)"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise IngredienteNaoEncontrado(ingrediente_id)

    db.delete(ingrediente)
    db.commit()
    return None


@router.patch("/{ingrediente_id}/disponibilidade", response_model=IngredienteResponse)
def alternar_disponibilidade(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """Alterna disponibilidade do ingrediente (admin only)"""
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        raise IngredienteNaoEncontrado(ingrediente_id)

    ingrediente.disponivel = not ingrediente.disponivel
    db.commit()
    db.refresh(ingrediente)
    return ingrediente
