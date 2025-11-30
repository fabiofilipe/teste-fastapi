"""Testes unitários para modelos"""
import pytest
import bcrypt
from app.models.models import Usuario, Produto, Pedido, ItemPedido


class TestUsuarioModel:
    """Testes do modelo Usuario"""

    def test_criar_usuario(self, db):
        """Testa criação de usuário"""
        senha_hash = bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()).decode()
        usuario = Usuario(
            nome="João Silva",
            email="joao@exemplo.com",
            senha=senha_hash,
            ativo=True,
            admin=False
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        assert usuario.id is not None
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@exemplo.com"
        assert usuario.ativo is True
        assert usuario.admin is False

    def test_usuario_email_unico(self, db, usuario_teste):
        """Testa que email deve ser único"""
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


class TestProdutoModel:
    """Testes do modelo Produto"""

    def test_criar_produto(self, db):
        """Testa criação de produto"""
        produto = Produto(
            nome="Pizza Margherita",
            descricao="Molho, mussarela e manjericão",
            categoria="PIZZA",
            tamanho="MEDIA",
            preco=35.00,
            disponivel=True
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.id is not None
        assert produto.nome == "Pizza Margherita"
        assert produto.categoria == "PIZZA"
        assert produto.tamanho == "MEDIA"
        assert produto.preco == 35.00
        assert produto.disponivel is True

    def test_produto_nome_tamanho_unico(self, db, produto_teste):
        """Testa que combinação nome+tamanho deve ser única"""
        from sqlalchemy.exc import IntegrityError

        produto_duplicado = Produto(
            nome=produto_teste.nome,
            categoria="PIZZA",
            tamanho=produto_teste.tamanho,
            preco=40.00,
            disponivel=True
        )
        db.add(produto_duplicado)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_produto_disponibilidade_padrao(self, db):
        """Testa que disponível é True por padrão"""
        produto = Produto(
            nome="Pizza Calabresa",
            categoria="PIZZA",
            tamanho="GRANDE",
            preco=45.00
        )
        db.add(produto)
        db.commit()
        db.refresh(produto)

        assert produto.disponivel is True


class TestPedidoModel:
    """Testes do modelo Pedido"""

    def test_criar_pedido(self, db, usuario_teste):
        """Testa criação de pedido"""
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
        """Testa relacionamento com usuário"""
        assert pedido_teste.usuario.id == usuario_teste.id
        assert pedido_teste.usuario.nome == usuario_teste.nome

    def test_pedido_relacionamento_itens(self, db, pedido_teste):
        """Testa relacionamento com itens"""
        assert len(pedido_teste.itens) == 1
        assert pedido_teste.itens[0].sabor == "Margherita"

    def test_pedido_status_padrao(self, db, usuario_teste):
        """Testa que status padrão é PENDENTE"""
        pedido = Pedido(
            usuario_id=usuario_teste.id,
            preco_total=30.00
        )
        db.add(pedido)
        db.commit()
        db.refresh(pedido)

        assert pedido.status == "PENDENTE"

    def test_pedido_preco_total_padrao(self, db, usuario_teste):
        """Testa que preço total padrão é 0.0"""
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

    def test_criar_item_pedido(self, db, pedido_teste):
        """Testa criação de item de pedido"""
        item = ItemPedido(
            pedido_id=pedido_teste.id,
            quantidade=2,
            sabor="Calabresa",
            tamanho="GRANDE",
            preco_unitario=45.00,
            observacoes="Sem cebola"
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        assert item.id is not None
        assert item.quantidade == 2
        assert item.sabor == "Calabresa"
        assert item.tamanho == "GRANDE"
        assert item.preco_unitario == 45.00
        assert item.observacoes == "Sem cebola"

    def test_item_relacionamento_pedido(self, db, pedido_teste):
        """Testa relacionamento com pedido"""
        item = pedido_teste.itens[0]
        assert item.pedido.id == pedido_teste.id
        assert item.pedido.usuario_id == pedido_teste.usuario_id

    def test_item_observacoes_opcional(self, db, pedido_teste):
        """Testa que observações é opcional"""
        item = ItemPedido(
            pedido_id=pedido_teste.id,
            quantidade=1,
            sabor="Margherita",
            tamanho="MEDIA",
            preco_unitario=35.00
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        assert item.observacoes is None
