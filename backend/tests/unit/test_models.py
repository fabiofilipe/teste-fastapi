"""Testes unitarios para modelos"""
import pytest
import bcrypt
from datetime import datetime
from app.models.models import Usuario, Produto, Pedido, ItemPedido, Endereco


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


class TestProdutoModel:
    """Testes do modelo Produto"""

    def test_criar_produto(self, db):
        """Testa criacao de produto"""
        produto = Produto(
            nome="Pizza Margherita",
            descricao="Molho, mussarela e manjericao",
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
        """Testa que combinacao nome+tamanho deve ser unica"""
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
        """Testa que disponivel e True por padrao"""
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
        assert pedido_teste.itens[0].sabor == "Margherita"

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

    def test_criar_item_pedido(self, db, pedido_teste):
        """Testa criacao de item de pedido"""
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
        """Testa que observacoes e opcional"""
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

    def test_produto_created_at_automatico(self, db):
        """Testa que created_at e preenchido em Produto"""
        produto = Produto(
            nome="Produto Timestamp",
            categoria="PIZZA",
            tamanho="MEDIA",
            preco=30.00
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

