"""Testes unitarios para modelos"""
import pytest
import bcrypt
from datetime import datetime
from app.models.models import (
    Usuario, Produto, Pedido, ItemPedido, Endereco,
    Categoria, Ingrediente, ProdutoVariacao, ProdutoIngrediente
)


class TestUsuarioModel:
    """Testes do modelo Usuario"""

    def test_criar_usuario(self, db):
        """Testa criacao de usuario"""
        senha_hash = bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()).decode()
        usuario = Usuario(
            nome="Joao Silva",
            email="joao@exemplo.com",
            senha=senha_hash,
            ativo=True,
            admin=False
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        assert usuario.id is not None
        assert usuario.nome == "Joao Silva"
        assert usuario.email == "joao@exemplo.com"
        assert usuario.ativo is True
        assert usuario.admin is False

    def test_usuario_email_unico(self, db, usuario_teste):
        """Testa que email deve ser unico"""
        from sqlalchemy.exc import IntegrityError

        usuario_duplicado = Usuario(
            nome="Outro Usuario",
            email=usuario_teste.email,
            senha="hash123",
            ativo=True,
            admin=False
        )
        db.add(usuario_duplicado)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_usuario_relacionamento_pedidos(self, db, usuario_teste):
        """Testa relacionamento com pedidos"""
        pedido = Pedido(
            usuario_id=usuario_teste.id,
            status="PENDENTE",
            preco_total=50.00
        )
        db.add(pedido)
        db.commit()

        db.refresh(usuario_teste)
        assert len(usuario_teste.pedidos) == 1
        assert usuario_teste.pedidos[0].status == "PENDENTE"




class TestPedidoModel:
    """Testes do modelo Pedido"""

    def test_criar_pedido(self, db, usuario_teste):
        """Testa criacao de pedido"""
        pedido = Pedido(
            usuario_id=usuario_teste.id,
            status="PENDENTE",
            preco_total=50.00
        )
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.id is not None
        assert pedido.status == "PENDENTE"
        assert pedido.preco_total == 50.00
        assert pedido.usuario_id == usuario_teste.id

    def test_pedido_relacionamento_usuario(self, db, pedido_teste, usuario_teste):
        """Testa relacionamento com usuario"""
        assert pedido_teste.usuario.id == usuario_teste.id
        assert pedido_teste.usuario.nome == usuario_teste.nome

    def test_pedido_relacionamento_itens(self, db, pedido_teste):
        """Testa relacionamento com itens"""
        assert len(pedido_teste.itens) == 1
        assert pedido_teste.itens[0].produto_nome == "Pizza Margherita"

    def test_pedido_status_padrao(self, db, usuario_teste):
        """Testa que status padrao e PENDENTE"""
        pedido = Pedido(
            usuario_id=usuario_teste.id,
            preco_total=30.00
        )
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.status == "PENDENTE"

    def test_pedido_preco_total_padrao(self, db, usuario_teste):
        """Testa que preco total padrao e 0.0"""
        pedido = Pedido(
            usuario_id=usuario_teste.id,
            status="PENDENTE"
        )
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.preco_total == 0.0


class TestItemPedidoModel:
    """Testes do modelo ItemPedido"""

    def test_criar_item_pedido(self, db, pedido_teste, produto_variacao_teste):
        """Testa criacao de item de pedido"""
        item = ItemPedido(
            pedido_id=pedido_teste.id,
            produto_variacao_id=produto_variacao_teste.id,
            quantidade=2,
            produto_nome="Pizza Calabresa",
            tamanho="GRANDE",
            preco_base=45.00,
            preco_ingredientes=0.0,
            preco_total=90.00,
            observacoes="Sem cebola"
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        assert item.id is not None
        assert item.quantidade == 2
        assert item.produto_nome == "Pizza Calabresa"
        assert item.tamanho == "GRANDE"
        assert item.preco_base == 45.00
        assert item.observacoes == "Sem cebola"

    def test_item_relacionamento_pedido(self, db, pedido_teste):
        """Testa relacionamento com pedido"""
        item = pedido_teste.itens[0]
        assert item.pedido.id == pedido_teste.id
        assert item.pedido.usuario_id == pedido_teste.usuario_id

    def test_item_observacoes_opcional(self, db, pedido_teste, produto_variacao_teste):
        """Testa que observacoes e opcional"""
        item = ItemPedido(
            pedido_id=pedido_teste.id,
            produto_variacao_id=produto_variacao_teste.id,
            quantidade=1,
            produto_nome="Pizza Margherita",
            tamanho="MEDIA",
            preco_base=35.00,
            preco_ingredientes=0.0,
            preco_total=35.00
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        assert item.observacoes is None


class TestTimestampMixin:
    """Testes para campos de timestamp automaticos"""

    def test_usuario_created_at_automatico(self, db):
        """Testa que created_at e preenchido automaticamente"""
        usuario = Usuario(
            nome="Teste Timestamp",
            email="timestamp@teste.com",
            senha="hash123"
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        assert usuario.created_at is not None
        assert isinstance(usuario.created_at, datetime)

    def test_produto_created_at_automatico(self, db, categoria_teste):
        """Testa que created_at e preenchido em Produto"""
        produto = Produto(
            nome="Produto Timestamp",
            categoria_id=categoria_teste.id,
            disponivel=True
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.created_at is not None
        assert produto.updated_at is not None

    def test_pedido_created_at_automatico(self, db, usuario_teste):
        """Testa que created_at e preenchido em Pedido"""
        pedido = Pedido(usuario_id=usuario_teste.id)
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.created_at is not None


class TestSoftDeleteMixin:
    """Testes para soft delete"""

    def test_usuario_deleted_at_nulo_por_padrao(self, db):
        """Testa que deleted_at e None por padrao"""
        usuario = Usuario(
            nome="Teste SoftDelete",
            email="softdelete@teste.com",
            senha="hash123"
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        assert usuario.deleted_at is None
        assert usuario.is_deleted is False

    def test_soft_delete_usuario(self, db):
        """Testa soft delete de usuario"""
        usuario = Usuario(
            nome="Usuario Para Deletar",
            email="deletar@teste.com",
            senha="hash123"
        )
        db.add(usuario)
        db.commit()

        usuario.soft_delete()
        db.commit()
        db.refresh(usuario)

        assert usuario.deleted_at is not None
        assert usuario.is_deleted is True

    def test_restore_usuario(self, db):
        """Testa restauracao de usuario deletado"""
        usuario = Usuario(
            nome="Usuario Para Restaurar",
            email="restaurar@teste.com",
            senha="hash123"
        )
        db.add(usuario)
        db.commit()

        usuario.soft_delete()
        db.commit()
        assert usuario.is_deleted is True

        usuario.restore()
        db.commit()
        db.refresh(usuario)

        assert usuario.deleted_at is None
        assert usuario.is_deleted is False


class TestEnderecoModel:
    """Testes do modelo Endereco"""

    def test_criar_endereco(self, db, usuario_teste):
        """Testa criacao de endereco"""
        endereco = Endereco(
            usuario_id=usuario_teste.id,
            rua="Rua das Flores",
            numero="123",
            complemento="Apto 45",
            bairro="Centro",
            cidade="Sao Paulo",
            estado="SP",
            cep="01234-567",
            is_default=True
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

        assert endereco.id is not None
        assert endereco.rua == "Rua das Flores"
        assert endereco.numero == "123"
        assert endereco.bairro == "Centro"
        assert endereco.cidade == "Sao Paulo"
        assert endereco.estado == "SP"
        assert endereco.cep == "01234-567"
        assert endereco.is_default is True

    def test_endereco_relacionamento_usuario(self, db, usuario_teste):
        """Testa relacionamento com usuario"""
        endereco = Endereco(
            usuario_id=usuario_teste.id,
            rua="Rua Teste",
            numero="100",
            bairro="Bairro",
            cidade="Cidade",
            estado="RJ",
            cep="12345678"
        )
        db.add(endereco)
        db.commit()
        db.refresh(usuario_teste)

        assert len(usuario_teste.enderecos) == 1
        assert usuario_teste.enderecos[0].rua == "Rua Teste"

    def test_endereco_complemento_opcional(self, db, usuario_teste):
        """Testa que complemento e opcional"""
        endereco = Endereco(
            usuario_id=usuario_teste.id,
            rua="Rua Sem Complemento",
            numero="50",
            bairro="Bairro",
            cidade="Cidade",
            estado="MG",
            cep="98765432"
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

        assert endereco.complemento is None

    def test_usuario_multiplos_enderecos(self, db, usuario_teste):
        """Testa que usuario pode ter multiplos enderecos"""
        endereco1 = Endereco(
            usuario_id=usuario_teste.id,
            rua="Endereco 1",
            numero="1",
            bairro="Bairro",
            cidade="Cidade",
            estado="SP",
            cep="11111111",
            is_default=True
        )
        endereco2 = Endereco(
            usuario_id=usuario_teste.id,
            rua="Endereco 2",
            numero="2",
            bairro="Bairro",
            cidade="Cidade",
            estado="SP",
            cep="22222222",
            is_default=False
        )
        db.add_all([endereco1, endereco2])
        db.commit()
        db.refresh(usuario_teste)

        assert len(usuario_teste.enderecos) == 2

    def test_pedido_com_endereco_entrega(self, db, usuario_teste):
        """Testa pedido com endereco de entrega"""
        endereco = Endereco(
            usuario_id=usuario_teste.id,
            rua="Rua Entrega",
            numero="999",
            bairro="Bairro",
            cidade="Cidade",
            estado="SP",
            cep="99999999"
        )
        db.add(endereco)
        db.commit()
        db.refresh(endereco)

        pedido = Pedido(
            usuario_id=usuario_teste.id,
            endereco_entrega_id=endereco.id
        )
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.endereco_entrega is not None
        assert pedido.endereco_entrega.rua == "Rua Entrega"


class TestCategoriaModel:
    """Testes do modelo Categoria"""

    def test_criar_categoria(self, db):
        """Testa criacao de categoria"""
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

        assert categoria.id is not None
        assert categoria.nome == "Pizzas"
        assert categoria.descricao == "Pizzas tradicionais e especiais"
        assert categoria.icone == "🍕"
        assert categoria.ordem_exibicao == 1
        assert categoria.ativa is True

    def test_categoria_nome_unico(self, db):
        """Testa que nome de categoria deve ser unico"""
        from sqlalchemy.exc import IntegrityError

        categoria1 = Categoria(nome="Pizzas", ordem_exibicao=1)
        db.add(categoria1)
        db.commit()

        categoria2 = Categoria(nome="Pizzas", ordem_exibicao=2)
        db.add(categoria2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_categoria_campos_opcionais(self, db):
        """Testa que descricao e icone sao opcionais"""
        categoria = Categoria(
            nome="Bebidas",
            ordem_exibicao=2
        )
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        assert categoria.descricao is None
        assert categoria.icone is None

    def test_categoria_ativa_padrao(self, db):
        """Testa que ativa e True por padrao"""
        categoria = Categoria(
            nome="Sobremesas",
            ordem_exibicao=3
        )
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        assert categoria.ativa is True

    def test_categoria_ordem_exibicao_padrao(self, db):
        """Testa que ordem_exibicao tem padrao 0"""
        categoria = Categoria(nome="Nova Categoria")
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        assert categoria.ordem_exibicao == 0

    def test_categoria_relacionamento_produtos(self, db, categoria_teste):
        """Testa relacionamento com produtos"""
        produto = Produto(
            categoria_id=categoria_teste.id,
            nome="Pizza Margherita",
            disponivel=True
        )
        db.add(produto)
        db.commit()

        db.refresh(categoria_teste)
        assert len(categoria_teste.produtos) == 1
        assert categoria_teste.produtos[0].nome == "Pizza Margherita"


class TestIngredienteModel:
    """Testes do modelo Ingrediente"""

    def test_criar_ingrediente(self, db):
        """Testa criacao de ingrediente"""
        ingrediente = Ingrediente(
            nome="Mussarela",
            preco_adicional=0.0,
            disponivel=True
        )
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)

        assert ingrediente.id is not None
        assert ingrediente.nome == "Mussarela"
        assert ingrediente.preco_adicional == 0.0
        assert ingrediente.disponivel is True

    def test_ingrediente_nome_unico(self, db):
        """Testa que nome de ingrediente deve ser unico"""
        from sqlalchemy.exc import IntegrityError

        ing1 = Ingrediente(nome="Tomate", preco_adicional=1.0)
        db.add(ing1)
        db.commit()

        ing2 = Ingrediente(nome="Tomate", preco_adicional=2.0)
        db.add(ing2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_ingrediente_preco_padrao(self, db):
        """Testa que preco_adicional tem padrao 0.0"""
        ingrediente = Ingrediente(nome="Oregano")
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)

        assert ingrediente.preco_adicional == 0.0

    def test_ingrediente_disponivel_padrao(self, db):
        """Testa que disponivel e True por padrao"""
        ingrediente = Ingrediente(nome="Manjericao", preco_adicional=1.5)
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)

        assert ingrediente.disponivel is True


class TestProdutoVariacaoModel:
    """Testes do modelo ProdutoVariacao"""

    def test_criar_variacao(self, db, produto_teste):
        """Testa criacao de variacao de produto"""
        variacao = ProdutoVariacao(
            produto_id=produto_teste.id,
            tamanho="GIGANTE",
            preco=55.00,
            disponivel=True
        )
        db.add(variacao)
        db.commit()
        db.refresh(variacao)

        assert variacao.id is not None
        assert variacao.produto_id == produto_teste.id
        assert variacao.tamanho == "GIGANTE"
        assert variacao.preco == 55.00
        assert variacao.disponivel is True

    def test_variacao_produto_tamanho_unico(self, db, categoria_teste):
        """Testa que combinacao produto+tamanho deve ser unica"""
        from sqlalchemy.exc import IntegrityError

        # Criar novo produto para testar uniqueness
        produto_novo = Produto(
            categoria_id=categoria_teste.id,
            nome="Produto Teste Uniqueness",
            disponivel=True
        )
        db.add(produto_novo)
        db.commit()
        db.refresh(produto_novo)

        var1 = ProdutoVariacao(
            produto_id=produto_novo.id,
            tamanho="GRANDE",
            preco=45.00
        )
        db.add(var1)
        db.commit()

        var2 = ProdutoVariacao(
            produto_id=produto_novo.id,
            tamanho="GRANDE",
            preco=50.00
        )
        db.add(var2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_variacao_disponivel_padrao(self, db, categoria_teste):
        """Testa que disponivel e True por padrao"""
        # Criar novo produto para testar
        produto_novo = Produto(
            categoria_id=categoria_teste.id,
            nome="Produto Teste Padrao",
            disponivel=True
        )
        db.add(produto_novo)
        db.commit()
        db.refresh(produto_novo)

        variacao = ProdutoVariacao(
            produto_id=produto_novo.id,
            tamanho="PEQUENA",
            preco=20.00
        )
        db.add(variacao)
        db.commit()
        db.refresh(variacao)

        assert variacao.disponivel is True

    def test_variacao_relacionamento_produto(self, db, produto_teste):
        """Testa relacionamento com produto"""
        db.refresh(produto_teste)
        assert len(produto_teste.variacoes) == 3  # fixture cria 3 variacoes
        assert all(v.produto_id == produto_teste.id for v in produto_teste.variacoes)


class TestProdutoIngredienteModel:
    """Testes do modelo ProdutoIngrediente"""

    def test_criar_produto_ingrediente(self, db, produto_teste, ingrediente_teste):
        """Testa criacao de associacao produto-ingrediente"""
        prod_ing = ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingrediente_teste.id,
            quantidade=1,
            obrigatorio=False
        )
        db.add(prod_ing)
        db.commit()
        db.refresh(prod_ing)

        assert prod_ing.id is not None
        assert prod_ing.produto_id == produto_teste.id
        assert prod_ing.ingrediente_id == ingrediente_teste.id
        assert prod_ing.quantidade == 1
        assert prod_ing.obrigatorio is False

    def test_produto_ingrediente_unico(self, db, produto_teste, ingrediente_teste):
        """Testa que combinacao produto+ingrediente deve ser unica"""
        from sqlalchemy.exc import IntegrityError

        prod_ing1 = ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingrediente_teste.id
        )
        db.add(prod_ing1)
        db.commit()

        prod_ing2 = ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingrediente_teste.id
        )
        db.add(prod_ing2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_produto_ingrediente_quantidade_padrao(self, db, produto_teste, ingrediente_teste):
        """Testa que quantidade tem padrao 1"""
        prod_ing = ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingrediente_teste.id
        )
        db.add(prod_ing)
        db.commit()
        db.refresh(prod_ing)

        assert prod_ing.quantidade == 1

    def test_produto_ingrediente_obrigatorio_padrao(self, db, produto_teste, ingrediente_teste):
        """Testa que obrigatorio e False por padrao"""
        prod_ing = ProdutoIngrediente(
            produto_id=produto_teste.id,
            ingrediente_id=ingrediente_teste.id
        )
        db.add(prod_ing)
        db.commit()
        db.refresh(prod_ing)

        assert prod_ing.obrigatorio is False

    def test_produto_ingrediente_relacionamentos(self, db, produto_com_ingredientes):
        """Testa relacionamentos produto-ingrediente"""
        db.refresh(produto_com_ingredientes)
        assert len(produto_com_ingredientes.ingredientes) == 3

        # Verificar que os ingredientes tem o relacionamento inverso
        for prod_ing in produto_com_ingredientes.ingredientes:
            assert prod_ing.produto.id == produto_com_ingredientes.id
            assert prod_ing.ingrediente is not None


class TestProdutoNovoModel:
    """Testes do novo modelo Produto com categorias e variacoes"""

    def test_criar_produto_novo(self, db, categoria_teste):
        """Testa criacao do novo modelo de produto"""
        produto = Produto(
            categoria_id=categoria_teste.id,
            nome="Pizza Calabresa",
            descricao="Calabresa e cebola",
            imagem_url="https://example.com/calabresa.jpg",
            disponivel=True
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.id is not None
        assert produto.categoria_id == categoria_teste.id
        assert produto.nome == "Pizza Calabresa"
        assert produto.descricao == "Calabresa e cebola"
        assert produto.imagem_url == "https://example.com/calabresa.jpg"
        assert produto.disponivel is True

    def test_produto_nome_unico(self, db, categoria_teste, produto_teste):
        """Testa que nome de produto deve ser unico"""
        from sqlalchemy.exc import IntegrityError

        produto_duplicado = Produto(
            categoria_id=categoria_teste.id,
            nome=produto_teste.nome,
            disponivel=True
        )
        db.add(produto_duplicado)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_produto_disponivel_padrao(self, db, categoria_teste):
        """Testa que disponivel e True por padrao"""
        produto = Produto(
            categoria_id=categoria_teste.id,
            nome="Pizza Portuguesa"
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.disponivel is True

    def test_produto_campos_opcionais(self, db, categoria_teste):
        """Testa que descricao e imagem_url sao opcionais"""
        produto = Produto(
            categoria_id=categoria_teste.id,
            nome="Pizza Simples"
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.descricao is None
        assert produto.imagem_url is None

    def test_produto_relacionamento_categoria(self, db, produto_teste, categoria_teste):
        """Testa relacionamento com categoria"""
        assert produto_teste.categoria.id == categoria_teste.id
        assert produto_teste.categoria.nome == categoria_teste.nome

    def test_produto_relacionamento_variacoes(self, db, produto_teste):
        """Testa relacionamento com variacoes"""
        db.refresh(produto_teste)
        assert len(produto_teste.variacoes) == 3
        assert all(v.produto_id == produto_teste.id for v in produto_teste.variacoes)

    def test_produto_delete_cascade_variacoes(self, db, produto_teste):
        """Testa que deletar produto deleta suas variacoes"""
        produto_id = produto_teste.id
        variacoes_ids = [v.id for v in produto_teste.variacoes]

        db.delete(produto_teste)
        db.commit()

        # Verificar que produto foi deletado
        assert db.query(Produto).filter(Produto.id == produto_id).first() is None

        # Verificar que variacoes foram deletadas em cascade
        for var_id in variacoes_ids:
            assert db.query(ProdutoVariacao).filter(ProdutoVariacao.id == var_id).first() is None

