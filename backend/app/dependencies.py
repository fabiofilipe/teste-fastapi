"""Dependências reutilizáveis para autenticação e autorização"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Usuario
from app.config import SECRET_KEY, ALGORITHM


# Schema de segurança Bearer
security = HTTPBearer()


def obter_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependência que valida o token JWT e retorna o usuário autenticado

    Args:
        credentials: Credenciais Bearer token do header Authorization
        db: Sessão do banco de dados

    Returns:
        Usuario autenticado

    Raises:
        HTTPException: Se token inválido ou usuário não encontrado
    """
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")

        if usuario_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Buscar usuário no banco
    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if usuario is None:
        raise credentials_exception

    # Verificar se usuário está ativo
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    return usuario


def obter_usuario_admin(
    usuario_atual: Usuario = Depends(obter_usuario_atual)
) -> Usuario:
    """
    Dependência que verifica se o usuário autenticado é administrador

    Args:
        usuario_atual: Usuário obtido da dependência obter_usuario_atual

    Returns:
        Usuario administrador

    Raises:
        HTTPException: Se usuário não for administrador
    """
    if not usuario_atual.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem realizar esta ação."
        )

    return usuario_atual
