"""Schemas Pydantic para validação e serialização"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Schemas de Usuário
class UsuarioSchema(BaseModel):
    """Schema para criação de usuário"""
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6)
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True


class UsuarioResponse(BaseModel):
    """Schema para resposta de usuário (sem senha)"""
    id: int
    nome: str
    email: str
    ativo: bool
    admin: bool

    class Config:
        from_attributes = True


# Schemas de Autenticação
class LoginSchema(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema para resposta de token JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token"""
    refresh_token: str

    class Config:
        from_attributes = True


# Schemas de Produto
class ProdutoCreate(BaseModel):
    """Schema para criação de produto"""
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = None
    categoria: str = Field(..., pattern="^(PIZZA|BEBIDA|SOBREMESA|ADICIONAL)$")
    tamanho: str = Field(..., pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE|UNICO)$")
    preco: float = Field(..., ge=0)
    disponivel: Optional[bool] = True

    class Config:
        from_attributes = True


class ProdutoUpdate(BaseModel):
    """Schema para atualização de produto"""
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = None
    categoria: Optional[str] = Field(None, pattern="^(PIZZA|BEBIDA|SOBREMESA|ADICIONAL)$")
    tamanho: Optional[str] = Field(None, pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE|UNICO)$")
    preco: Optional[float] = Field(None, ge=0)
    disponivel: Optional[bool] = None

    class Config:
        from_attributes = True


class ProdutoResponse(BaseModel):
    """Schema para resposta de produto"""
    id: int
    nome: str
    descricao: Optional[str]
    categoria: str
    tamanho: str
    preco: float
    disponivel: bool

    class Config:
        from_attributes = True


# Schemas de Item do Pedido
class ItemPedidoCreate(BaseModel):
    """Schema para criação de item do pedido"""
    quantidade: int = Field(..., ge=1)
    sabor: str = Field(..., min_length=3)
    tamanho: str = Field(..., pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE)$")
    preco_unitario: float = Field(..., ge=0)
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True


class ItemPedidoResponse(BaseModel):
    """Schema para resposta de item do pedido"""
    id: int
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    observacoes: Optional[str]

    class Config:
        from_attributes = True


# Schemas de Pedido
class PedidoCreate(BaseModel):
    """Schema para criação de pedido"""
    itens: Optional[List[ItemPedidoCreate]] = []

    class Config:
        from_attributes = True


class PedidoResponse(BaseModel):
    """Schema para resposta de pedido"""
    id: int
    status: str
    usuario_id: int
    preco_total: float
    itens: List[ItemPedidoResponse] = []

    class Config:
        from_attributes = True
