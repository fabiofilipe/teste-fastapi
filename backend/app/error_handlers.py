"""Handlers para tratamento de erros global"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose.exceptions import JWTError

from app.exceptions import PizzariaException


async def pizzaria_exception_handler(request: Request, exc: PizzariaException):
    """Handler para exceções customizadas da pizzaria"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Erro de validação nos dados fornecidos",
            "details": errors,
            "path": str(request.url)
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler para erros do SQLAlchemy"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "message": "Erro ao processar operação no banco de dados",
            "path": str(request.url)
        }
    )


async def jwt_exception_handler(request: Request, exc: JWTError):
    """Handler para erros de JWT"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "JWTError",
            "message": "Token inválido ou expirado",
            "path": str(request.url)
        },
        headers={"WWW-Authenticate": "Bearer"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para exceções não tratadas"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "Erro interno do servidor",
            "path": str(request.url)
        }
    )
