"""
Sistema de Gerenciamento de Pizzaria - Backend API
FastAPI application para gerenciamento de pedidos de pizzaria
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth_router, orders_router

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

# Registrar routers
app.include_router(auth_router)
app.include_router(orders_router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz da API"""
    return {
        "mensagem": "Bem-vindo à API da Pizzaria!",
        "documentacao": "/docs",
        "versao": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "healthy"}
