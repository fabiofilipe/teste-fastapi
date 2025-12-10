"""Routers da API"""
from app.routers.auth import router as auth_router
from app.routers.orders import router as orders_router
from app.routers.products import router as products_router
from app.routers.health import router as health_router
from app.routers.categorias import router as categorias_router
from app.routers.ingredientes import router as ingredientes_router
from app.routers.cardapio import router as cardapio_router

__all__ = [
    "auth_router",
    "orders_router",
    "products_router",
    "health_router",
    "categorias_router",
    "ingredientes_router",
    "cardapio_router"
]
