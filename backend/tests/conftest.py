"""Configurações e fixtures globais para os testes"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.models import Usuario, Produto, Pedido, ItemPedido
import bcrypt


# Database de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture que cria um banco de dados limpo para cada teste"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture que cria um cliente de teste HTTP"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_teste(db):
    """Fixture que cria um usuário de teste"""
    senha_hash = bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()).decode()
    usuario = Usuario(
        nome="Usuario Teste",
        email="teste@exemplo.com",
        senha=senha_hash,
        ativo=True,
        admin=False
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture
def admin_teste(db):
    """Fixture que cria um usuário admin de teste"""
    senha_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    admin = Usuario(
        nome="Admin Teste",
        email="admin@exemplo.com",
        senha=senha_hash,
        ativo=True,
        admin=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def token_usuario(client, usuario_teste):
    """Fixture que retorna token JWT de um usuário comum"""
    response = client.post(
        "/auth/login",
        json={
            "email": "teste@exemplo.com",
            "password": "senha123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def token_admin(client, admin_teste):
    """Fixture que retorna token JWT de um admin"""
    response = client.post(
        "/auth/login",
        json={
            "email": "admin@exemplo.com",
            "password": "admin123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def produto_teste(db):
    """Fixture que cria um produto de teste"""
    produto = Produto(
        nome="Pizza Margherita",
        descricao="Molho de tomate, mussarela e manjericão",
        categoria="PIZZA",
        tamanho="MEDIA",
        preco=35.00,
        disponivel=True
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


@pytest.fixture
def produtos_diversos(db):
    """Fixture que cria vários produtos para testes"""
    produtos = [
        Produto(nome="Pizza Calabresa", categoria="PIZZA", tamanho="GRANDE", preco=45.00, disponivel=True),
        Produto(nome="Pizza Portuguesa", categoria="PIZZA", tamanho="MEDIA", preco=40.00, disponivel=True),
        Produto(nome="Coca-Cola", categoria="BEBIDA", tamanho="UNICO", preco=8.00, disponivel=True),
        Produto(nome="Brownie", categoria="SOBREMESA", tamanho="UNICO", preco=12.00, disponivel=False),
    ]
    db.add_all(produtos)
    db.commit()
    for produto in produtos:
        db.refresh(produto)
    return produtos


@pytest.fixture
def pedido_teste(db, usuario_teste, produto_teste):
    """Fixture que cria um pedido de teste"""
    pedido = Pedido(
        usuario_id=usuario_teste.id,
        status="PENDENTE",
        preco_total=35.00
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    # Adicionar item ao pedido
    item = ItemPedido(
        pedido_id=pedido.id,
        quantidade=1,
        sabor="Margherita",
        tamanho="MEDIA",
        preco_unitario=35.00
    )
    db.add(item)
    db.commit()

    return pedido
