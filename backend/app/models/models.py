"""Modelos SQLAlchemy para o sistema de pizzaria"""
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Usuario(Base):
    """Modelo de usuário do sistema"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    # Relacionamento com pedidos
    pedidos = relationship("Pedido", back_populates="usuario")

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    """Modelo de pedido"""
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String, default="PENDENTE")  # PENDENTE, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    preco_total = Column(Float, default=0.0)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    def __init__(self, usuario_id, status="PENDENTE", preco_total=0.0):
        self.usuario_id = usuario_id
        self.status = status
        self.preco_total = preco_total


class ItemPedido(Base):
    """Modelo de item do pedido (pizza)"""
    __tablename__ = "itens_pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    sabor = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)  # PEQUENA, MEDIA, GRANDE, GIGANTE
    preco_unitario = Column(Float, nullable=False)
    observacoes = Column(String, nullable=True)

    # Relacionamento
    pedido = relationship("Pedido", back_populates="itens")

    def __init__(self, pedido_id, quantidade, sabor, tamanho, preco_unitario, observacoes=None):
        self.pedido_id = pedido_id
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.observacoes = observacoes
