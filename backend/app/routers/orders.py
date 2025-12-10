"""Rotas de gerenciamento de pedidos"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Tuple

from app.database import get_db
from app.models.models import (
    Pedido, ItemPedido, Usuario, Produto, ProdutoVariacao,
    Ingrediente, ProdutoIngrediente
)
from app.schemas.schemas import PedidoCreate, PedidoResponse
from app.dependencies.auth import obter_usuario_atual, obter_usuario_admin
from app.exceptions import (
    ProdutoNaoEncontrado, StatusInvalido, SemPermissao,
    PedidoNaoEncontrado, ProdutoVariacaoNaoEncontrada,
    IngredienteNaoEncontrado, IngredienteIndisponivel,
    IngredienteObrigatorio
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def calcular_preco_item(
    produto_variacao: ProdutoVariacao,
    ingredientes_adicionados: List[int],
    ingredientes_removidos: List[int],
    quantidade: int,
    db: Session
) -> Tuple[float, float, float, list, list]:
    """
    Calcula preco de um item do pedido com customizacoes

    Retorna: (preco_base, preco_ingredientes, preco_total,
              ingredientes_adicionados_data, ingredientes_removidos_data)
    """
    preco_base = produto_variacao.preco
    preco_ingredientes = 0.0

    # Validar e adicionar ingredientes extras
    ingredientes_adicionados_data = []
    for ing_id in ingredientes_adicionados:
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ing_id).first()
        if not ingrediente:
            raise IngredienteNaoEncontrado(ing_id)
        if not ingrediente.disponivel:
            raise IngredienteIndisponivel(ingrediente.nome)

        preco_ingredientes += ingrediente.preco_adicional
        ingredientes_adicionados_data.append({
            "id": ingrediente.id,
            "nome": ingrediente.nome,
            "preco": ingrediente.preco_adicional
        })

    # Validar ingredientes removidos
    ingredientes_removidos_data = []
    for ing_id in ingredientes_removidos:
        # Verificar se ingrediente esta nos ingredientes padrao do produto
        produto_ingrediente = db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.produto_id == produto_variacao.produto_id,
            ProdutoIngrediente.ingrediente_id == ing_id
        ).first()

        if not produto_ingrediente:
            continue  # Ignorar se nao e um ingrediente padrao

        if produto_ingrediente.obrigatorio:
            raise IngredienteObrigatorio(produto_ingrediente.ingrediente.nome)

        ingredientes_removidos_data.append({
            "id": produto_ingrediente.ingrediente.id,
            "nome": produto_ingrediente.ingrediente.nome
        })

    preco_total = (preco_base + preco_ingredientes) * quantidade

    return preco_base, preco_ingredientes, preco_total, ingredientes_adicionados_data, ingredientes_removidos_data


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

    - **itens**: Lista de itens do pedido com produto_variacao_id e customizações

    Útil para mostrar o valor total antes de confirmar o pedido.
    """
    preco_total = 0.0
    itens_calculados = []

    for item_data in pedido.itens:
        # Buscar a variacao do produto
        produto_variacao = db.query(ProdutoVariacao)\
            .filter(ProdutoVariacao.id == item_data.produto_variacao_id)\
            .first()

        if not produto_variacao:
            raise ProdutoVariacaoNaoEncontrada(item_data.produto_variacao_id)

        # Verificar se a variacao esta disponivel
        if not produto_variacao.disponivel or not produto_variacao.produto.disponivel:
            raise ProdutoNaoEncontrado(produto_variacao.produto_id)

        # Calcular preco com customizacoes
        preco_base, preco_ingredientes, preco_item, ing_adicionados, ing_removidos = calcular_preco_item(
            produto_variacao,
            item_data.ingredientes_adicionados or [],
            item_data.ingredientes_removidos or [],
            item_data.quantidade,
            db
        )

        preco_total += preco_item

        itens_calculados.append({
            "produto_id": produto_variacao.produto_id,
            "produto_nome": produto_variacao.produto.nome,
            "tamanho": produto_variacao.tamanho,
            "quantidade": item_data.quantidade,
            "preco_base": preco_base,
            "preco_ingredientes": preco_ingredientes,
            "preco_total_item": round(preco_item, 2),
            "ingredientes_adicionados": ing_adicionados,
            "ingredientes_removidos": ing_removidos
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

    - **itens**: Lista de itens do pedido com produto_variacao_id e customizações

    O pedido será criado para o usuário autenticado.
    Os preços são calculados automaticamente baseados no cardápio e customizações.
    """
    # Criar o pedido para o usuario autenticado
    novo_pedido = Pedido(
        usuario_id=usuario_atual.id,
        endereco_entrega_id=pedido.endereco_entrega_id
    )
    db.add(novo_pedido)
    db.flush()  # Flush para obter o ID do pedido

    # Adicionar os itens ao pedido com validacao de produtos e customizacoes
    preco_total = 0.0
    for item_data in pedido.itens:
        # Buscar a variacao do produto
        produto_variacao = db.query(ProdutoVariacao)\
            .join(Produto)\
            .filter(ProdutoVariacao.id == item_data.produto_variacao_id)\
            .first()

        if not produto_variacao:
            raise ProdutoVariacaoNaoEncontrada(item_data.produto_variacao_id)

        # Verificar se o produto e variacao estao disponiveis
        if not produto_variacao.disponivel or not produto_variacao.produto.disponivel:
            from app.exceptions import PizzariaException
            raise PizzariaException(
                f"Produto '{produto_variacao.produto.nome}' ({produto_variacao.tamanho}) não está disponível",
                status.HTTP_400_BAD_REQUEST
            )

        # Calcular preco com customizacoes
        preco_base, preco_ingredientes, preco_item, ing_adicionados, ing_removidos = calcular_preco_item(
            produto_variacao,
            item_data.ingredientes_adicionados or [],
            item_data.ingredientes_removidos or [],
            item_data.quantidade,
            db
        )

        # Criar item do pedido com snapshot e customizacoes
        item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_variacao_id=produto_variacao.id,
            quantidade=item_data.quantidade,
            # Snapshot (historico)
            produto_nome=produto_variacao.produto.nome,
            tamanho=produto_variacao.tamanho,
            preco_base=preco_base,
            # Customizacoes
            ingredientes_adicionados=ing_adicionados,
            ingredientes_removidos=ing_removidos,
            preco_ingredientes=preco_ingredientes,
            preco_total=preco_item,
            observacoes=item_data.observacoes
        )
        preco_total += preco_item
        db.add(item)

    # Atualizar o preco total do pedido
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
