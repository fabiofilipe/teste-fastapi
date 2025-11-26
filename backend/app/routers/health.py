"""Router para healthcheck e métricas do sistema"""
from fastapi import APIRouter, Depends, status as http_status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import os

from app.database import get_db
from app.models import Usuario, Pedido, Produto


router = APIRouter(tags=["Health & Metrics"])


@router.get("/health", summary="Verificação de saúde da API")
async def health_check(db: Session = Depends(get_db)):
    """
    Verifica o status de saúde da API e suas dependências

    Retorna:
    - Status da API
    - Status da conexão com banco de dados
    - Timestamp da verificação
    """
    # Verificar conexão com banco de dados
    db_status = "healthy"
    db_message = "Conexão com banco de dados OK"

    try:
        # Tentar executar uma query simples
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "unhealthy"
        db_message = f"Erro na conexão com banco: {str(e)}"

    overall_status = "healthy" if db_status == "healthy" else "unhealthy"

    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "api": "healthy",
            "database": {
                "status": db_status,
                "message": db_message
            }
        }
    }


@router.get("/metrics", summary="Métricas do sistema")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Retorna métricas básicas do sistema

    Inclui:
    - Total de usuários
    - Total de pedidos
    - Total de produtos
    - Estatísticas de pedidos por status
    - Valor total em pedidos
    """
    # Contar totais
    total_usuarios = db.query(Usuario).count()
    total_pedidos = db.query(Pedido).count()
    total_produtos = db.query(Produto).count()
    produtos_disponiveis = db.query(Produto).filter(Produto.disponivel == True).count()

    # Estatísticas de pedidos
    pedidos = db.query(Pedido).all()

    pedidos_por_status = {
        "PENDENTE": 0,
        "EM_PREPARO": 0,
        "PRONTO": 0,
        "ENTREGUE": 0,
        "CANCELADO": 0
    }

    valor_total_pedidos = 0.0
    for pedido in pedidos:
        if pedido.status in pedidos_por_status:
            pedidos_por_status[pedido.status] += 1
        valor_total_pedidos += pedido.preco_total

    # Calcular valor médio
    valor_medio_pedido = round(valor_total_pedidos / total_pedidos, 2) if total_pedidos > 0 else 0

    return {
        "timestamp": datetime.now().isoformat(),
        "usuarios": {
            "total": total_usuarios,
            "ativos": db.query(Usuario).filter(Usuario.ativo == True).count(),
            "admins": db.query(Usuario).filter(Usuario.admin == True).count()
        },
        "produtos": {
            "total": total_produtos,
            "disponiveis": produtos_disponiveis,
            "indisponiveis": total_produtos - produtos_disponiveis
        },
        "pedidos": {
            "total": total_pedidos,
            "por_status": pedidos_por_status,
            "valor_total": round(valor_total_pedidos, 2),
            "valor_medio": valor_medio_pedido
        }
    }


@router.get("/info", summary="Informações sobre a API")
async def api_info():
    """
    Retorna informações gerais sobre a API

    Inclui:
    - Nome e versão da API
    - Ambiente de execução
    - Endpoints disponíveis
    - Documentação
    """
    return {
        "name": "API Pizzaria",
        "version": "1.0.0",
        "description": "Sistema de gerenciamento de pedidos para pizzaria",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "metrics": "/metrics"
        },
        "features": [
            "Autenticação JWT com refresh token",
            "CRUD de usuários, produtos e pedidos",
            "Validação automática de preços",
            "Sistema de permissões (admin/usuário)",
            "Tratamento de erros global",
            "Estatísticas de pedidos"
        ],
        "contact": {
            "documentation": "/docs"
        }
    }


@router.get("/status", summary="Status completo do sistema")
async def system_status(db: Session = Depends(get_db)):
    """
    Retorna status completo do sistema combinando health e métricas

    Útil para dashboards de monitoramento
    """
    # Verificar saúde do banco
    db_healthy = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_healthy = False

    # Métricas básicas
    total_pedidos = db.query(Pedido).count()
    total_usuarios = db.query(Usuario).count()
    total_produtos = db.query(Produto).count()

    # Pedidos ativos (não entregues ou cancelados)
    pedidos_ativos = db.query(Pedido).filter(
        Pedido.status.in_(["PENDENTE", "EM_PREPARO", "PRONTO"])
    ).count()

    return {
        "timestamp": datetime.now().isoformat(),
        "status": "operational" if db_healthy else "degraded",
        "database": "connected" if db_healthy else "disconnected",
        "api_version": "1.0.0",
        "summary": {
            "total_usuarios": total_usuarios,
            "total_produtos": total_produtos,
            "total_pedidos": total_pedidos,
            "pedidos_ativos": pedidos_ativos
        },
        "uptime": "Sistema em execução",
        "endpoints": {
            "health_details": "/health",
            "full_metrics": "/metrics",
            "api_info": "/info"
        }
    }
