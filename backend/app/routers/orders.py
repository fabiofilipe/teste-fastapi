"""Rotas de gerenciamento de pedidos"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Pedido, ItemPedido, Usuario
from app.schemas import PedidoCreate, PedidoResponse, ItemPedidoCreate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/", summary="Listar todos os pedidos")
async def listar_pedidos(db: Session = Depends(get_db)):
    """
    Lista todos os pedidos da pizzaria

    Retorna todos os pedidos com seus itens
    """
    pedidos = db.query(Pedido).all()
    return {"total": len(pedidos), "pedidos": pedidos}


@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Buscar pedido por ID")
async def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Busca um pedido específico pelo ID

    - **pedido_id**: ID do pedido
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado"
        )

    return pedido


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo pedido")
async def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo pedido para a pizzaria

    - **usuario_id**: ID do usuário que está fazendo o pedido
    - **itens**: Lista de itens do pedido (pizzas)
    """
    # Verifica se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.id == pedido.usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário {pedido.usuario_id} não encontrado"
        )

    # Cria o pedido
    novo_pedido = Pedido(usuario_id=pedido.usuario_id)
    db.add(novo_pedido)
    db.flush()  # Flush para obter o ID do pedido

    # Adiciona os itens ao pedido
    preco_total = 0.0
    for item_data in pedido.itens:
        item = ItemPedido(
            pedido_id=novo_pedido.id,
            quantidade=item_data.quantidade,
            sabor=item_data.sabor,
            tamanho=item_data.tamanho,
            preco_unitario=item_data.preco_unitario,
            observacoes=item_data.observacoes
        )
        preco_total += item.quantidade * item.preco_unitario
        db.add(item)

    # Atualiza o preço total do pedido
    novo_pedido.preco_total = preco_total

    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.patch("/{pedido_id}/status", summary="Atualizar status do pedido")
async def atualizar_status(
    pedido_id: int,
    novo_status: str,
    db: Session = Depends(get_db)
):
    """
    Atualiza o status de um pedido

    - **pedido_id**: ID do pedido
    - **novo_status**: Novo status (PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO)
    """
    status_validos = ["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE", "CANCELADO"]

    if novo_status not in status_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status inválido. Use um dos seguintes: {', '.join(status_validos)}"
        )

    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado"
        )

    pedido.status = novo_status
    db.commit()
    db.refresh(pedido)

    return {
        "mensagem": f"Status do pedido {pedido_id} atualizado para {novo_status}",
        "pedido": pedido
    }


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Cancelar pedido")
async def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Cancela um pedido (deleta do banco de dados)

    - **pedido_id**: ID do pedido a ser cancelado
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pedido {pedido_id} não encontrado"
        )

    db.delete(pedido)
    db.commit()

    return None
