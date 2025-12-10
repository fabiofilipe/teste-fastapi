"""Configurações e fixtures globais para os testes"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.models import (
    Usuario, Produto, Pedido, ItemPedido,
    Categoria, Ingrediente, ProdutoVariacao, ProdutoIngrediente
)
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
            "senha": "senha123"
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
            "senha": "admin123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def categoria_teste(db):
    """Fixture que cria uma categoria de teste"""
    categoria = Categoria(
        nome="Pizzas",
        descricao="Pizzas tradicionais e especiais",
        icone="🍕",
        ordem_exibicao=1,
        ativa=True
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@pytest.fixture
def categorias_diversas(db):
    """Fixture que cria várias categorias para testes"""
    categorias = [
        Categoria(nome="Pizzas", descricao="Pizzas deliciosas", icone="🍕", ordem_exibicao=1, ativa=True),
        Categoria(nome="Bebidas", descricao="Bebidas refrescantes", icone="🥤", ordem_exibicao=2, ativa=True),
        Categoria(nome="Sobremesas", descricao="Sobremesas doces", icone="🍰", ordem_exibicao=3, ativa=True),
        Categoria(nome="Inativa", descricao="Categoria inativa", icone="❌", ordem_exibicao=4, ativa=False),
    ]
    db.add_all(categorias)
    db.commit()
    for cat in categorias:
        db.refresh(cat)
    return categorias


@pytest.fixture
def ingrediente_teste(db):
    """Fixture que cria um ingrediente de teste"""
    ingrediente = Ingrediente(
        nome="Mussarela",
        preco_adicional=0.0,
        disponivel=True
    )
    db.add(ingrediente)
    db.commit()
    db.refresh(ingrediente)
    return ingrediente


@pytest.fixture
def ingredientes_diversos(db):
    """Fixture que cria vários ingredientes para testes"""
    ingredientes = [
        Ingrediente(nome="Mussarela", preco_adicional=0.0, disponivel=True),
        Ingrediente(nome="Tomate", preco_adicional=1.0, disponivel=True),
        Ingrediente(nome="Manjericão", preco_adicional=1.5, disponivel=True),
        Ingrediente(nome="Calabresa", preco_adicional=3.0, disponivel=True),
        Ingrediente(nome="Bacon", preco_adicional=3.5, disponivel=False),  # Indisponível
    ]
    db.add_all(ingredientes)
    db.commit()
    for ing in ingredientes:
        db.refresh(ing)
    return ingredientes


@pytest.fixture
def produto_teste(db, categoria_teste):
    """Fixture que cria um produto de teste com variações"""
    produto = Produto(
        categoria_id=categoria_teste.id,
        nome="Pizza Margherita",
        descricao="Molho de tomate, mussarela e manjericão",
        imagem_url="https://example.com/margherita.jpg",
        disponivel=True
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)

    # Adicionar variações
    variacoes = [
        ProdutoVariacao(produto_id=produto.id, tamanho="PEQUENA", preco=25.00, disponivel=True),
        ProdutoVariacao(produto_id=produto.id, tamanho="MEDIA", preco=35.00, disponivel=True),
        ProdutoVariacao(produto_id=produto.id, tamanho="GRANDE", preco=45.00, disponivel=True),
    ]
    db.add_all(variacoes)
    db.commit()
    for var in variacoes:
        db.refresh(var)

    produto.variacoes = variacoes
    return produto


@pytest.fixture
def produto_variacao_teste(db, produto_teste):
    """Fixture que retorna uma variação de produto de teste"""
    return produto_teste.variacoes[1]  # Retorna a variação MEDIA


@pytest.fixture
def produto_com_ingredientes(db, produto_teste, ingredientes_diversos):
    """Fixture que cria um produto com ingredientes padrão"""
    # Adicionar ingredientes padrão ao produto
    produto_ingredientes = [
        ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingredientes_diversos[0].id,  # Mussarela
            obrigatorio=True
        ),
        ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingredientes_diversos[1].id,  # Tomate
            obrigatorio=False
        ),
        ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingredientes_diversos[2].id,  # Manjericão
            obrigatorio=False
        ),
    ]
    db.add_all(produto_ingredientes)
    db.commit()

    db.refresh(produto_teste)
    return produto_teste


@pytest.fixture
def produtos_diversos(db, categorias_diversas):
    """Fixture que cria vários produtos para testes com variações"""
    cat_pizza = categorias_diversas[0]
    cat_bebida = categorias_diversas[1]
    cat_sobremesa = categorias_diversas[2]

    # Pizza Calabresa
    p1 = Produto(categoria_id=cat_pizza.id, nome="Pizza Calabresa", descricao="Calabresa e cebola", disponivel=True)
    db.add(p1)
    db.flush()
    db.add(ProdutoVariacao(produto_id=p1.id, tamanho="GRANDE", preco=45.00, disponivel=True))

    # Pizza Portuguesa
    p2 = Produto(categoria_id=cat_pizza.id, nome="Pizza Portuguesa", descricao="Presunto e ovos", disponivel=True)
    db.add(p2)
    db.flush()
    db.add(ProdutoVariacao(produto_id=p2.id, tamanho="MEDIA", preco=40.00, disponivel=True))

    # Coca-Cola
    p3 = Produto(categoria_id=cat_bebida.id, nome="Coca-Cola", descricao="Refrigerante", disponivel=True)
    db.add(p3)
    db.flush()
    db.add(ProdutoVariacao(produto_id=p3.id, tamanho="UNICO", preco=8.00, disponivel=True))

    # Brownie (indisponível)
    p4 = Produto(categoria_id=cat_sobremesa.id, nome="Brownie", descricao="Brownie de chocolate", disponivel=False)
    db.add(p4)
    db.flush()
    db.add(ProdutoVariacao(produto_id=p4.id, tamanho="UNICO", preco=12.00, disponivel=False))

    db.commit()
    produtos = [p1, p2, p3, p4]
    for produto in produtos:
        db.refresh(produto)
    return produtos


@pytest.fixture
def pedido_teste(db, usuario_teste, produto_variacao_teste):
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
        produto_variacao_id=produto_variacao_teste.id,
        quantidade=1,
        produto_nome="Pizza Margherita",
        tamanho="MEDIA",
        preco_base=35.00,
        ingredientes_adicionados=[],
        ingredientes_removidos=[],
        preco_ingredientes=0.0,
        preco_total=35.00
    )
    db.add(item)
    db.commit()

    return pedido


@pytest.fixture
def cardapio_completo(db, categorias_diversas, produtos_diversos, ingredientes_diversos):
    """Fixture que cria um cardápio completo para testes"""
    # Associar alguns ingredientes aos produtos
    produto_pizza = produtos_diversos[0]  # Pizza Calabresa

    produto_ingredientes = [
        ProdutoIngrediente(
            produto_id=produto_pizza.id,
            ingrediente_id=ingredientes_diversos[0].id,  # Mussarela
            obrigatorio=True
        ),
        ProdutoIngrediente(
            produto_id=produto_pizza.id,
            ingrediente_id=ingredientes_diversos[3].id,  # Calabresa
            obrigatorio=False
        ),
    ]
    db.add_all(produto_ingredientes)
    db.commit()

    return {
        "categorias": categorias_diversas,
        "produtos": produtos_diversos,
        "ingredientes": ingredientes_diversos
    }
