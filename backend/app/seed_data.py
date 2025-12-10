"""
Script para popular o banco de dados com dados iniciais
Execute: python -m app.seed_data
"""
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.models import (
    Base, Categoria, Ingrediente, Produto, ProdutoVariacao,
    ProdutoIngrediente, Usuario
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_categorias(db: Session):
    """Criar categorias do cardápio"""
    categorias = [
        {
            "nome": "Pizzas",
            "descricao": "Pizzas tradicionais e especiais",
            "icone": "🍕",
            "ordem_exibicao": 1,
            "ativa": True
        },
        {
            "nome": "Bebidas",
            "descricao": "Refrigerantes, sucos e águas",
            "icone": "🥤",
            "ordem_exibicao": 2,
            "ativa": True
        },
        {
            "nome": "Sobremesas",
            "descricao": "Doces e sobremesas deliciosas",
            "icone": "🍰",
            "ordem_exibicao": 3,
            "ativa": True
        }
    ]

    categorias_criadas = []
    for cat_data in categorias:
        categoria = Categoria(**cat_data)
        db.add(categoria)
        categorias_criadas.append(categoria)

    db.flush()
    print(f"✓ {len(categorias_criadas)} categorias criadas")
    return categorias_criadas


def criar_ingredientes(db: Session):
    """Criar ingredientes disponíveis"""
    ingredientes = [
        {"nome": "Mussarela", "preco_adicional": 0.0, "disponivel": True},
        {"nome": "Presunto", "preco_adicional": 2.5, "disponivel": True},
        {"nome": "Calabresa", "preco_adicional": 3.0, "disponivel": True},
        {"nome": "Catupiry", "preco_adicional": 4.0, "disponivel": True},
        {"nome": "Bacon", "preco_adicional": 3.5, "disponivel": True},
        {"nome": "Cebola", "preco_adicional": 1.0, "disponivel": True},
        {"nome": "Tomate", "preco_adicional": 1.0, "disponivel": True},
        {"nome": "Azeitona", "preco_adicional": 1.5, "disponivel": True},
        {"nome": "Palmito", "preco_adicional": 4.5, "disponivel": True},
        {"nome": "Frango", "preco_adicional": 3.0, "disponivel": True},
        {"nome": "Milho", "preco_adicional": 1.0, "disponivel": True},
        {"nome": "Champignon", "preco_adicional": 3.5, "disponivel": True},
        {"nome": "Manjericão", "preco_adicional": 1.5, "disponivel": True},
        {"nome": "Orégano", "preco_adicional": 0.0, "disponivel": True},
        {"nome": "Parmesão", "preco_adicional": 2.0, "disponivel": True}
    ]

    ingredientes_criados = []
    for ing_data in ingredientes:
        ingrediente = Ingrediente(**ing_data)
        db.add(ingrediente)
        ingredientes_criados.append(ingrediente)

    db.flush()
    print(f"✓ {len(ingredientes_criados)} ingredientes criados")
    return ingredientes_criados


def criar_produtos_pizzas(db: Session, categoria_pizza, ingredientes_dict):
    """Criar produtos de pizza com variações e ingredientes padrão"""

    # Pizza Margherita
    margherita = Produto(
        categoria_id=categoria_pizza.id,
        nome="Pizza Margherita",
        descricao="Molho de tomate, mussarela, tomate fresco e manjericão",
        imagem_url="https://example.com/margherita.jpg",
        disponivel=True
    )
    db.add(margherita)
    db.flush()

    # Variações de tamanho
    for tamanho, preco in [("PEQUENA", 25.0), ("MEDIA", 35.0), ("GRANDE", 45.0)]:
        variacao = ProdutoVariacao(
            produto_id=margherita.id,
            tamanho=tamanho,
            preco=preco,
            disponivel=True
        )
        db.add(variacao)

    # Ingredientes padrão
    for nome_ing in ["Mussarela", "Tomate", "Manjericão", "Orégano"]:
        if nome_ing in ingredientes_dict:
            prod_ing = ProdutoIngrediente(
                produto_id=margherita.id,
                ingrediente_id=ingredientes_dict[nome_ing].id,
                obrigatorio=(nome_ing == "Mussarela")
            )
            db.add(prod_ing)

    # Pizza Calabresa
    calabresa = Produto(
        categoria_id=categoria_pizza.id,
        nome="Pizza Calabresa",
        descricao="Molho de tomate, mussarela, calabresa e cebola",
        imagem_url="https://example.com/calabresa.jpg",
        disponivel=True
    )
    db.add(calabresa)
    db.flush()

    for tamanho, preco in [("PEQUENA", 28.0), ("MEDIA", 38.0), ("GRANDE", 48.0)]:
        variacao = ProdutoVariacao(
            produto_id=calabresa.id,
            tamanho=tamanho,
            preco=preco,
            disponivel=True
        )
        db.add(variacao)

    for nome_ing in ["Mussarela", "Calabresa", "Cebola", "Orégano"]:
        if nome_ing in ingredientes_dict:
            prod_ing = ProdutoIngrediente(
                produto_id=calabresa.id,
                ingrediente_id=ingredientes_dict[nome_ing].id,
                obrigatorio=(nome_ing == "Mussarela")
            )
            db.add(prod_ing)

    # Pizza Frango com Catupiry
    frango_cat = Produto(
        categoria_id=categoria_pizza.id,
        nome="Pizza Frango com Catupiry",
        descricao="Molho de tomate, mussarela, frango desfiado e catupiry",
        imagem_url="https://example.com/frango-catupiry.jpg",
        disponivel=True
    )
    db.add(frango_cat)
    db.flush()

    for tamanho, preco in [("PEQUENA", 30.0), ("MEDIA", 40.0), ("GRANDE", 50.0)]:
        variacao = ProdutoVariacao(
            produto_id=frango_cat.id,
            tamanho=tamanho,
            preco=preco,
            disponivel=True
        )
        db.add(variacao)

    for nome_ing in ["Mussarela", "Frango", "Catupiry", "Milho", "Orégano"]:
        if nome_ing in ingredientes_dict:
            prod_ing = ProdutoIngrediente(
                produto_id=frango_cat.id,
                ingrediente_id=ingredientes_dict[nome_ing].id,
                obrigatorio=(nome_ing == "Mussarela")
            )
            db.add(prod_ing)

    # Pizza Portuguesa
    portuguesa = Produto(
        categoria_id=categoria_pizza.id,
        nome="Pizza Portuguesa",
        descricao="Molho de tomate, mussarela, presunto, ovos, cebola e azeitona",
        imagem_url="https://example.com/portuguesa.jpg",
        disponivel=True
    )
    db.add(portuguesa)
    db.flush()

    for tamanho, preco in [("PEQUENA", 32.0), ("MEDIA", 42.0), ("GRANDE", 52.0)]:
        variacao = ProdutoVariacao(
            produto_id=portuguesa.id,
            tamanho=tamanho,
            preco=preco,
            disponivel=True
        )
        db.add(variacao)

    for nome_ing in ["Mussarela", "Presunto", "Cebola", "Azeitona", "Orégano"]:
        if nome_ing in ingredientes_dict:
            prod_ing = ProdutoIngrediente(
                produto_id=portuguesa.id,
                ingrediente_id=ingredientes_dict[nome_ing].id,
                obrigatorio=(nome_ing == "Mussarela")
            )
            db.add(prod_ing)

    # Pizza Quatro Queijos
    quatro_queijos = Produto(
        categoria_id=categoria_pizza.id,
        nome="Pizza Quatro Queijos",
        descricao="Mussarela, catupiry, parmesão e provolone",
        imagem_url="https://example.com/quatro-queijos.jpg",
        disponivel=True
    )
    db.add(quatro_queijos)
    db.flush()

    for tamanho, preco in [("PEQUENA", 35.0), ("MEDIA", 45.0), ("GRANDE", 55.0)]:
        variacao = ProdutoVariacao(
            produto_id=quatro_queijos.id,
            tamanho=tamanho,
            preco=preco,
            disponivel=True
        )
        db.add(variacao)

    for nome_ing in ["Mussarela", "Catupiry", "Parmesão", "Orégano"]:
        if nome_ing in ingredientes_dict:
            prod_ing = ProdutoIngrediente(
                produto_id=quatro_queijos.id,
                ingrediente_id=ingredientes_dict[nome_ing].id,
                obrigatorio=True
            )
            db.add(prod_ing)

    print(f"✓ 5 pizzas criadas com variações e ingredientes padrão")


def criar_produtos_bebidas(db: Session, categoria_bebida):
    """Criar produtos de bebidas"""
    bebidas = [
        {
            "nome": "Coca-Cola",
            "descricao": "Refrigerante de cola",
            "variacoes": [
                {"tamanho": "UNICO", "preco": 5.0}
            ]
        },
        {
            "nome": "Guaraná Antarctica",
            "descricao": "Refrigerante de guaraná",
            "variacoes": [
                {"tamanho": "UNICO", "preco": 5.0}
            ]
        },
        {
            "nome": "Suco de Laranja",
            "descricao": "Suco natural de laranja",
            "variacoes": [
                {"tamanho": "PEQUENA", "preco": 6.0},
                {"tamanho": "GRANDE", "preco": 10.0}
            ]
        }
    ]

    for bebida_data in bebidas:
        bebida = Produto(
            categoria_id=categoria_bebida.id,
            nome=bebida_data["nome"],
            descricao=bebida_data["descricao"],
            disponivel=True
        )
        db.add(bebida)
        db.flush()

        for var_data in bebida_data["variacoes"]:
            variacao = ProdutoVariacao(
                produto_id=bebida.id,
                tamanho=var_data["tamanho"],
                preco=var_data["preco"],
                disponivel=True
            )
            db.add(variacao)

    print(f"✓ {len(bebidas)} bebidas criadas")


def criar_produtos_sobremesas(db: Session, categoria_sobremesa):
    """Criar produtos de sobremesas"""
    sobremesas = [
        {
            "nome": "Petit Gateau",
            "descricao": "Bolo de chocolate com sorvete de baunilha",
            "variacoes": [
                {"tamanho": "UNICO", "preco": 15.0}
            ]
        },
        {
            "nome": "Brownie",
            "descricao": "Brownie de chocolate com nozes",
            "variacoes": [
                {"tamanho": "UNICO", "preco": 12.0}
            ]
        }
    ]

    for sobremesa_data in sobremesas:
        sobremesa = Produto(
            categoria_id=categoria_sobremesa.id,
            nome=sobremesa_data["nome"],
            descricao=sobremesa_data["descricao"],
            disponivel=True
        )
        db.add(sobremesa)
        db.flush()

        for var_data in sobremesa_data["variacoes"]:
            variacao = ProdutoVariacao(
                produto_id=sobremesa.id,
                tamanho=var_data["tamanho"],
                preco=var_data["preco"],
                disponivel=True
            )
            db.add(variacao)

    print(f"✓ {len(sobremesas)} sobremesas criadas")


def criar_usuario_admin(db: Session):
    """Criar usuário administrador padrão"""
    admin = Usuario(
        nome="Administrador",
        email="admin@pizzaria.com",
        senha=pwd_context.hash("admin123"),
        admin=True,
        ativo=True
    )
    db.add(admin)
    db.flush()
    print(f"✓ Usuário admin criado (email: admin@pizzaria.com, senha: admin123)")

    # Criar usuário comum de teste
    usuario = Usuario(
        nome="Cliente Teste",
        email="cliente@teste.com",
        senha=pwd_context.hash("senha123"),
        admin=False,
        ativo=True
    )
    db.add(usuario)
    db.flush()
    print(f"✓ Usuário teste criado (email: cliente@teste.com, senha: senha123)")


def limpar_banco(db: Session):
    """Limpar todas as tabelas"""
    print("\n🗑️  Limpando banco de dados...")

    # Deletar na ordem correta devido às FKs
    db.query(ProdutoIngrediente).delete()
    db.query(ProdutoVariacao).delete()
    db.query(Produto).delete()
    db.query(Ingrediente).delete()
    db.query(Categoria).delete()
    db.query(Usuario).delete()

    db.commit()
    print("✓ Banco de dados limpo\n")


def popular_banco():
    """Função principal para popular o banco"""
    print("\n" + "="*60)
    print("🍕 SEED DATA - SISTEMA DE PIZZARIA")
    print("="*60 + "\n")

    # Criar as tabelas se não existirem
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Limpar banco
        limpar_banco(db)

        # Criar dados
        print("📝 Criando dados iniciais...\n")

        categorias = criar_categorias(db)
        ingredientes = criar_ingredientes(db)

        # Criar dicionário de ingredientes para fácil acesso
        ingredientes_dict = {ing.nome: ing for ing in ingredientes}

        # Criar produtos por categoria
        categoria_pizza = categorias[0]
        categoria_bebida = categorias[1]
        categoria_sobremesa = categorias[2]

        criar_produtos_pizzas(db, categoria_pizza, ingredientes_dict)
        criar_produtos_bebidas(db, categoria_bebida)
        criar_produtos_sobremesas(db, categoria_sobremesa)

        # Criar usuários
        criar_usuario_admin(db)

        db.commit()

        print("\n" + "="*60)
        print("✅ SEED DATA CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print("\n📊 Resumo:")
        print(f"   • 3 categorias")
        print(f"   • 15 ingredientes")
        print(f"   • 10 produtos (5 pizzas + 3 bebidas + 2 sobremesas)")
        print(f"   • 2 usuários (1 admin + 1 cliente)")
        print("\n🔑 Credenciais de acesso:")
        print("   Admin: admin@pizzaria.com / admin123")
        print("   Cliente: cliente@teste.com / senha123")
        print("\n🚀 Servidor: uvicorn app.main:app --reload")
        print("📖 Documentação: http://localhost:8000/docs")
        print("\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao popular banco: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()
