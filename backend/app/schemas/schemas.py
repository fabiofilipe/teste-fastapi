"""Schemas Pydantic para validacao e serializacao"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# Schemas de Usuario
class UsuarioSchema(BaseModel):
    """Schema para criacao de usuario"""
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6)
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True


class UsuarioResponse(BaseModel):
    """Schema para resposta de usuario (sem senha)"""
    id: int
    nome: str
    email: str
    ativo: bool
    admin: bool

    class Config:
        from_attributes = True


# Schemas de Autenticacao
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
    """Schema para requisicao de refresh token"""
    refresh_token: str

    class Config:
        from_attributes = True


# Schemas de Endereco
class EnderecoCreate(BaseModel):
    """Schema para criacao de endereco"""
    rua: str = Field(..., min_length=3, max_length=200)
    numero: str = Field(..., min_length=1, max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: str = Field(..., min_length=2, max_length=100)
    cidade: str = Field(..., min_length=2, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)
    cep: str = Field(..., pattern=r"^\d{5}-?\d{3}$")
    is_default: Optional[bool] = False

    class Config:
        from_attributes = True


class EnderecoUpdate(BaseModel):
    """Schema para atualizacao de endereco"""
    rua: Optional[str] = Field(None, min_length=3, max_length=200)
    numero: Optional[str] = Field(None, min_length=1, max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, min_length=2, max_length=100)
    cidade: Optional[str] = Field(None, min_length=2, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    cep: Optional[str] = Field(None, pattern=r"^\d{5}-?\d{3}$")
    is_default: Optional[bool] = None

    class Config:
        from_attributes = True


class EnderecoResponse(BaseModel):
    """Schema para resposta de endereco"""
    id: int
    rua: str
    numero: str
    complemento: Optional[str]
    bairro: str
    cidade: str
    estado: str
    cep: str
    is_default: bool

    class Config:
        from_attributes = True


# Schemas de Produto
class ProdutoCreate(BaseModel):
    """Schema para criacao de produto"""
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = None
    categoria: str = Field(..., pattern="^(PIZZA|BEBIDA|SOBREMESA|ADICIONAL)$")
    tamanho: str = Field(..., pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE|UNICO)$")
    preco: float = Field(..., ge=0)
    disponivel: Optional[bool] = True

    class Config:
        from_attributes = True


class ProdutoUpdate(BaseModel):
    """Schema para atualizacao de produto"""
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
    """Schema para criacao de item do pedido"""
    produto_id: int = Field(..., gt=0, description="ID do produto no cardapio")
    quantidade: int = Field(..., ge=1)
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
    """Schema para criacao de pedido"""
    itens: Optional[List[ItemPedidoCreate]] = []
    endereco_entrega_id: Optional[int] = None

    class Config:
        from_attributes = True


class PedidoResponse(BaseModel):
    """Schema para resposta de pedido"""
    id: int
    status: str
    usuario_id: int
    preco_total: float
    itens: List[ItemPedidoResponse] = []
    endereco_entrega: Optional[EnderecoResponse] = None

    class Config:
        from_attributes = True


# Schemas de Categoria
class CategoriaCreate(BaseModel):
    """Schema para criacao de categoria"""
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = None
    icone: Optional[str] = None
    ordem_exibicao: int = Field(default=0, ge=0)
    ativa: Optional[bool] = True

    class Config:
        from_attributes = True


class CategoriaUpdate(BaseModel):
    """Schema para atualizacao de categoria"""
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = None
    icone: Optional[str] = None
    ordem_exibicao: Optional[int] = Field(None, ge=0)
    ativa: Optional[bool] = None

    class Config:
        from_attributes = True


class CategoriaResponse(BaseModel):
    """Schema para resposta de categoria"""
    id: int
    nome: str
    descricao: Optional[str]
    icone: Optional[str]
    ordem_exibicao: int
    ativa: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schemas de Ingrediente
class IngredienteCreate(BaseModel):
    """Schema para criacao de ingrediente"""
    nome: str = Field(..., min_length=2, max_length=100)
    preco_adicional: float = Field(default=0.0, ge=0)
    disponivel: Optional[bool] = True

    class Config:
        from_attributes = True


class IngredienteUpdate(BaseModel):
    """Schema para atualizacao de ingrediente"""
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    preco_adicional: Optional[float] = Field(None, ge=0)
    disponivel: Optional[bool] = None

    class Config:
        from_attributes = True


class IngredienteResponse(BaseModel):
    """Schema para resposta de ingrediente"""
    id: int
    nome: str
    preco_adicional: float
    disponivel: bool

    class Config:
        from_attributes = True


# Schemas de ProdutoVariacao
class ProdutoVariacaoCreate(BaseModel):
    """Schema para criacao de variacao de produto"""
    tamanho: str = Field(..., pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE|UNICO)$")
    preco: float = Field(..., gt=0)
    disponivel: Optional[bool] = True

    class Config:
        from_attributes = True


class ProdutoVariacaoUpdate(BaseModel):
    """Schema para atualizacao de variacao"""
    tamanho: Optional[str] = Field(None, pattern="^(PEQUENA|MEDIA|GRANDE|GIGANTE|UNICO)$")
    preco: Optional[float] = Field(None, gt=0)
    disponivel: Optional[bool] = None

    class Config:
        from_attributes = True


class ProdutoVariacaoResponse(BaseModel):
    """Schema para resposta de variacao"""
    id: int
    produto_id: int
    tamanho: str
    preco: float
    disponivel: bool

    class Config:
        from_attributes = True

