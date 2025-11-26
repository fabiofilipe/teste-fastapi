"""Rotas de gerenciamento de pedidos"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Pedido, ItemPedido, Usuario, Produto
from app.schemas import PedidoCreate, PedidoResponse, ItemPedidoCreate
from app.dependencies import obter_usuario_atual, obter_usuario_admin
from app.exceptions import ProdutoNaoEncontrado, ProdutoIndisponivel, StatusInvalido, SemPermissao, PedidoNaoEncontrado

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/meus/estatisticas", summary="Estatísticas dos meus pedidos")
async def estatisticas_meus_pedidos(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Retorna estatísticas dos pedidos do usuário autenticado

    Inclui total de pedidos, valor total gasto e contagem por status
    """
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == usuario_atual.id).all()

    # Calcular estatísticas
    total_pedidos = len(pedidos)
    valor_total = sum(p.preco_total for p in pedidos)

    # Contar por status
    status_count = {
        "PENDENTE": 0,
        "EM_PREPARO": 0,
        "PRONTO": 0,
        "ENTREGUE": 0,
        "CANCELADO": 0
    }

    for pedido in pedidos:
        if pedido.status in status_count:
            status_count[pedido.status] += 1

    return {
        "total_pedidos": total_pedidos,
        "valor_total_gasto": round(valor_total, 2),
        "pedidos_por_status": status_count,
        "valor_medio_pedido": round(valor_total / total_pedidos, 2) if total_pedidos > 0 else 0
    }


@router.get("/meus", response_model=List[PedidoResponse], summary="Listar meus pedidos")
async def listar_meus_pedidos(
    status_pedido: str = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Lista todos os pedidos do usuário autenticado

    - **status_pedido**: Filtro opcional por status (PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO)

    Retorna apenas os pedidos pertencentes ao usuário que fez a requisição
    """
    query = db.query(Pedido).filter(Pedido.usuario_id == usuario_atual.id)

    # Filtrar por status se fornecido
    if status_pedido:
        status_validos = ["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE", "CANCELADO"]
        if status_pedido.upper() not in status_validos:
            raise StatusInvalido(status_pedido, status_validos)
        query = query.filter(Pedido.status == status_pedido.upper())

    pedidos = query.all()
    return pedidos


@router.get("/", summary="Listar todos os pedidos")
async def listar_pedidos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """
    Lista todos os pedidos da pizzaria (apenas admin)

    Retorna todos os pedidos com seus itens
    """
    pedidos = db.query(Pedido).all()
    return {"total": len(pedidos), "pedidos": pedidos}


@router.get("/{pedido_id}", response_model=PedidoResponse, summary="Buscar pedido por ID")
async def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Busca um pedido específico pelo ID

    - **pedido_id**: ID do pedido
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise PedidoNaoEncontrado(pedido_id)

    # Verificar se o usuário é dono do pedido ou admin
    if pedido.usuario_id != usuario_atual.id and not usuario_atual.admin:
        raise SemPermissao("acessar este pedido")

    return pedido


@router.post("/calcular-preco", summary="Calcular preço do pedido antes de criar")
async def calcular_preco_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_atual)
):
    """
    Calcula o preço total de um pedido sem salvá-lo

    - **itens**: Lista de itens do pedido com produto_id do cardápio

    Útil para mostrar o valor total antes de confirmar o pedido.
    """
    preco_total = 0.0
    itens_calculados = []

    for item_data in pedido.itens:
        # Buscar o produto no cardápio
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()

        if not produto:
            raise ProdutoNaoEncontrado(item_data.produto_id)

        # Verificar se o produto está disponível
        if not produto.disponivel:
            raise ProdutoIndisponivel(produto.nome)

        # Calcular preço do item
        preco_item = produto.preco * item_data.quantidade
        preco_total += preco_item

        itens_calculados.append({
            "produto_id": produto.id,
            "produto_nome": produto.nome,
            "tamanho": produto.tamanho,
            "quantidade": item_data.quantidade,
            "preco_unitario": produto.preco,
            "preco_total_item": round(preco_item, 2)
        })

    return {
        "itens": itens_calculados,
        "preco_total": round(preco_total, 2),
        "quantidade_itens": len(itens_calculados)
    }


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED, summary="Criar novo pedido")
async def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Cria um novo pedido para a pizzaria

    - **itens**: Lista de itens do pedido com produto_id do cardápio

    O pedido será criado para o usuário autenticado.
    Os preços são calculados automaticamente baseados no cardápio.
    """
    # Cria o pedido para o usuário autenticado
    novo_pedido = Pedido(usuario_id=usuario_atual.id)
    db.add(novo_pedido)
    db.flush()  # Flush para obter o ID do pedido

    # Adiciona os itens ao pedido com validação de produtos
    preco_total = 0.0
    for item_data in pedido.itens:
        # Buscar o produto no cardápio
        produto = db.query(Produto).filter(Produto.id == item_data.produto_id).first()

        if not produto:
            raise ProdutoNaoEncontrado(item_data.produto_id)

        # Verificar se o produto está disponível
        if not produto.disponivel:
            raise ProdutoIndisponivel(produto.nome)

        # Criar item do pedido com dados do produto
        item = ItemPedido(
            pedido_id=novo_pedido.id,
            quantidade=item_data.quantidade,
            sabor=produto.nome,  # Nome do produto como sabor
            tamanho=produto.tamanho,
            preco_unitario=produto.preco,  # Preço do cardápio
            observacoes=item_data.observacoes
        )
        preco_total += item.quantidade * item.preco_unitario
        db.add(item)

    # Atualiza o preço total do pedido
    novo_pedido.preco_total = round(preco_total, 2)

    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.patch("/{pedido_id}/status", summary="Atualizar status do pedido")
async def atualizar_status(
    pedido_id: int,
    novo_status: str,
    db: Session = Depends(get_db),
    _: Usuario = Depends(obter_usuario_admin)
):
    """
    Atualiza o status de um pedido (apenas admin)

    - **pedido_id**: ID do pedido
    - **novo_status**: Novo status (PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO)
    """
    status_validos = ["PENDENTE", "EM_PREPARO", "PRONTO", "ENTREGUE", "CANCELADO"]

    if novo_status.upper() not in status_validos:
        raise StatusInvalido(novo_status, status_validos)

    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise PedidoNaoEncontrado(pedido_id)

    pedido.status = novo_status.upper()
    db.commit()
    db.refresh(pedido)

    return {
        "mensagem": f"Status do pedido {pedido_id} atualizado para {novo_status.upper()}",
        "pedido": pedido
    }


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Cancelar pedido")
async def cancelar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Cancela um pedido (deleta do banco de dados)

    - **pedido_id**: ID do pedido a ser cancelado

    Usuários podem cancelar seus próprios pedidos. Admins podem cancelar qualquer pedido.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise PedidoNaoEncontrado(pedido_id)

    # Verificar se o usuário é dono do pedido ou admin
    if pedido.usuario_id != usuario_atual.id and not usuario_atual.admin:
        raise SemPermissao("cancelar este pedido")

    db.delete(pedido)
    db.commit()

    return None
