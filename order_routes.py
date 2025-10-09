from fastapi  import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido
 
#order == Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    return {"Voce acessou a rota de pedidos "}

@order_router.post("/pedido")
async def criar_pedido(pedido_schemas: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(Usuario=pedido_schemas.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID pedido: {novo_pedido.id}"}