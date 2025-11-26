"""Rotas de autenticação"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioSchema, UsuarioResponse, LoginSchema, TokenResponse
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["Autenticação"])

# Contexto de criptografia
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_token(usuario_id: int, duracao_token: timedelta) -> str:
    """
    Cria um token JWT para o usuário

    Args:
        usuario_id: ID do usuário
        duracao_token: Duração de validade do token

    Returns:
        Token JWT codificado
    """
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    claims = {
        "sub": str(usuario_id),
        "exp": data_expiracao
    }
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def autenticar_usuario(email: str, senha: str, db: Session) -> Usuario | bool:
    """
    Autentica um usuário verificando email e senha

    Args:
        email: Email do usuário
        senha: Senha em texto plano
        db: Sessão do banco de dados

    Returns:
        Objeto Usuario se autenticado, False caso contrário
    """
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@router.get("/", summary="Rota inicial de autenticação")
async def home():
    """Rota inicial para verificar disponibilidade do serviço de autenticação"""
    return {
        "mensagem": "Serviço de autenticação da Pizzaria",
        "endpoints": ["/auth/criar_conta", "/auth/login"]
    }


@router.post("/criar_conta", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Criar nova conta")
async def criar_conta(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    """
    Cria uma nova conta de usuário

    - **nome**: Nome completo do usuário
    - **email**: Email único do usuário
    - **senha**: Senha (mínimo 6 caracteres)
    - **ativo**: Se o usuário está ativo (opcional, padrão: True)
    - **admin**: Se o usuário é administrador (opcional, padrão: False)
    """
    # Verifica se o email já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {usuario.email} já está cadastrado"
        )

    # Criptografa a senha
    senha_hash = bcrypt_context.hash(usuario.senha)

    # Cria novo usuário
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hash,
        ativo=usuario.ativo,
        admin=usuario.admin
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post("/login", response_model=TokenResponse, summary="Fazer login")
async def login(credenciais: LoginSchema, db: Session = Depends(get_db)):
    """
    Autentica um usuário e retorna tokens de acesso

    - **email**: Email do usuário
    - **senha**: Senha do usuário

    Retorna access_token (30min) e refresh_token (7 dias)
    """
    usuario = autenticar_usuario(credenciais.email, credenciais.senha, db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Entre em contato com o administrador."
        )

    # Cria tokens
    access_token = criar_token(
        usuario.id,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = criar_token(
        usuario.id,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
