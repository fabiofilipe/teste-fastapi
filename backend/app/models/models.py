"""Modelos SQLAlchemy para o sistema de pizzaria"""
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin


class Usuario(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de usuario do sistema"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    # Relacionamentos
    pedidos = relationship("Pedido", back_populates="usuario")
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")


class Endereco(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de endereco do usuario"""
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    rua = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False, index=True)
    is_default = Column(Boolean, default=False)

    # Relacionamento
    usuario = relationship("Usuario", back_populates="enderecos")


class Pedido(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de pedido"""
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="PENDENTE", index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    preco_total = Column(Float, default=0.0)
    endereco_entrega_id = Column(Integer, ForeignKey("enderecos.id"), nullable=True)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    endereco_entrega = relationship("Endereco")


class Categoria(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de categoria do cardapio"""
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    descricao = Column(String, nullable=True)
    icone = Column(String, nullable=True)  # URL ou emoji
    ordem_exibicao = Column(Integer, nullable=False, default=0, index=True)
    ativa = Column(Boolean, default=True, index=True)

    # Relacionamentos
    produtos = relationship("Produto", back_populates="categoria")


class Ingrediente(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de ingrediente para customizacao"""
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    preco_adicional = Column(Float, nullable=False, default=0.0)
    disponivel = Column(Boolean, default=True, index=True)

    # Relacionamentos
    produtos = relationship("ProdutoIngrediente", back_populates="ingrediente")


class ProdutoVariacao(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de variacao de produto (tamanhos/precos)"""
    __tablename__ = "produtos_variacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False, index=True)
    tamanho = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True, index=True)

    # Relacionamento
    produto = relationship("Produto", back_populates="variacoes")

    # Constraints
    __table_args__ = (
        UniqueConstraint('produto_id', 'tamanho', name='uq_produto_tamanho'),
    )


class Produto(Base, TimestampMixin, SoftDeleteMixin):
    """Modelo de produto do cardapio"""
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False, unique=True, index=True)
    descricao = Column(String, nullable=True)
    categoria = Column(String, nullable=False, index=True)
    tamanho = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True, index=True)


class ItemPedido(Base, TimestampMixin):
    """Modelo de item do pedido"""
    __tablename__ = "itens_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False, index=True)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    observacoes = Column(String, nullable=True)

    # Relacionamento
    pedido = relationship("Pedido", back_populates="itens")

