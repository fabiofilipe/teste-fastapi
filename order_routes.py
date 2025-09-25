from fastapi  import APIRouter

#order == Pedido

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/")
async def pedidos():
    return {"Voce acessou a rota de pedidos "}
