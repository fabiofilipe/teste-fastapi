from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#migração do banco de dados pelo alembic

#criando conexão
db = create_engine("sqlite:///banco.db")

#criando base banco de dados
Base = declarative_base()

# criando as classes/tabelas
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default= False)


    #ativo=True já inicia o usuario ativo
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome 
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"

#retirar Status_pedido, atualizar depois gerenciando o alembic
    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    status = Column("Status", String)#pendente, cancelado, finalizado #passando para string para evitar problemas com o alembic, Nova task arrumar isso
    Usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens = 
        
    def __init__(self, Usuario, status="PENDENTE", preco=0):
        self.Usuario = Usuario
        self.preco = preco
        self.status = status

class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True) 
    quantidade = Column("quantidade", Integer)
    sabor = Column("Sabor", String) # deixar generalizado, mas poderia criar uma nova tabela para sabor ou fazer um choice_type
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float) 
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido