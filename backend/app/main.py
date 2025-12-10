"""
Sistema de Gerenciamento de Pizzaria - Backend API
FastAPI application para gerenciamento de pedidos de pizzaria
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose.exceptions import JWTError

from app.database import engine, Base
from app.routers import (
    auth_router,
    orders_router,
    products_router,
    health_router,
    categorias_router,
    ingredientes_router,
    cardapio_router
)
from app.exceptions import PizzariaException
from app.error_handlers import (
    pizzaria_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    jwt_exception_handler,
    generic_exception_handler
)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="API Pizzaria",
    description="Sistema de gerenciamento de pedidos para pizzaria",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar exception handlers
app.add_exception_handler(PizzariaException, pizzaria_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(JWTError, jwt_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Registrar routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(ingredientes_router)
app.include_router(products_router)
app.include_router(cardapio_router)
app.include_router(orders_router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz da API"""
    return {
        "mensagem": "Bem-vindo à API da Pizzaria!",
        "versao": "1.0.0",
        "documentacao": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints_uteis": {
            "health": "/health",
            "metrics": "/metrics",
            "info": "/info"
        },
        "recursos": {
            "autenticacao": "/auth",
            "categorias": "/categorias",
            "ingredientes": "/ingredientes",
            "produtos": "/produtos",
            "cardapio": "/cardapio",
            "pedidos": "/pedidos"
        }
    }
