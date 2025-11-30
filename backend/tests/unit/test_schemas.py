"""Testes unitários para schemas Pydantic"""
import pytest
from pydantic import ValidationError
from app.schemas.schemas import (
    UsuarioSchema,
    UsuarioResponse,
    LoginSchema,
    ProdutoCreate,
    ProdutoResponse,
    ItemPedidoCreate,
    PedidoCreate
)


class TestUsuarioSchema:
    """Testes do schema UsuarioSchema"""

    def test_usuario_valido(self):
        """Testa criação de usuário válido"""
        usuario = UsuarioSchema(
            nome="João Silva",
            email="joao@exemplo.com",
            senha="senha123"
        )
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@exemplo.com"
        assert usuario.ativo is True
        assert usuario.admin is False

    def test_nome_muito_curto(self):
        """Testa que nome deve ter no mínimo 3 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioSchema(
                nome="Jo",
                email="joao@exemplo.com",
                senha="senha123"
            )
        assert "at least 3 characters" in str(exc_info.value)

    def test_email_invalido(self):
        """Testa validação de email inválido"""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioSchema(
                nome="João Silva",
                email="email-invalido",
                senha="senha123"
            )
        assert "value is not a valid email address" in str(exc_info.value)

    def test_senha_muito_curta(self):
        """Testa que senha deve ter no mínimo 6 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioSchema(
                nome="João Silva",
                email="joao@exemplo.com",
                senha="12345"
            )
        assert "at least 6 characters" in str(exc_info.value)


class TestLoginSchema:
    """Testes do schema LoginSchema"""

    def test_login_valido(self):
        """Testa criação de login válido"""
        login = LoginSchema(
            email="joao@exemplo.com",
            senha="senha123"
        )
        assert login.email == "joao@exemplo.com"
        assert login.senha == "senha123"

    def test_email_obrigatorio(self):
        """Testa que email é obrigatório"""
        with pytest.raises(ValidationError) as exc_info:
            LoginSchema(senha="senha123")
        assert "email" in str(exc_info.value).lower()


class TestProdutoSchema:
    """Testes dos schemas de Produto"""

    def test_produto_create_valido(self):
        """Testa criação de produto válido"""
        produto = ProdutoCreate(
            nome="Pizza Margherita",
            descricao="Molho, mussarela e manjericão",
            categoria="PIZZA",
            tamanho="MEDIA",
            preco=35.00
        )
        assert produto.nome == "Pizza Margherita"
        assert produto.categoria == "PIZZA"
        assert produto.tamanho == "MEDIA"
        assert produto.preco == 35.00

    def test_preco_negativo_invalido(self):
        """Testa que preço não pode ser negativo"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                nome="Pizza Margherita",
                categoria="PIZZA",
                tamanho="MEDIA",
                preco=-10.00
            )
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_categoria_invalida(self):
        """Testa validação de categoria"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                nome="Pizza Margherita",
                categoria="CATEGORIA_INVALIDA",
                tamanho="MEDIA",
                preco=35.00
            )
        assert "string should match pattern" in str(exc_info.value).lower()

    def test_tamanho_invalido(self):
        """Testa validação de tamanho"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                nome="Pizza Margherita",
                categoria="PIZZA",
                tamanho="ENORME",
                preco=35.00
            )
        assert "string should match pattern" in str(exc_info.value).lower()


class TestItemPedidoSchema:
    """Testes do schema ItemPedidoCreate"""

    def test_item_pedido_valido(self):
        """Testa criação de item de pedido válido"""
        item = ItemPedidoCreate(
            produto_id=1,
            quantidade=2
        )
        assert item.produto_id == 1
        assert item.quantidade == 2

    def test_quantidade_minima(self):
        """Testa que quantidade deve ser no mínimo 1"""
        with pytest.raises(ValidationError) as exc_info:
            ItemPedidoCreate(
                produto_id=1,
                quantidade=0
            )
        assert "greater than or equal to 1" in str(exc_info.value)

    def test_produto_id_obrigatorio(self):
        """Testa que produto_id é obrigatório"""
        with pytest.raises(ValidationError) as exc_info:
            ItemPedidoCreate(quantidade=1)
        assert "produto_id" in str(exc_info.value).lower()

    def test_produto_id_maior_que_zero(self):
        """Testa que produto_id deve ser maior que 0"""
        with pytest.raises(ValidationError) as exc_info:
            ItemPedidoCreate(produto_id=0, quantidade=1)
        assert "greater than 0" in str(exc_info.value)

    def test_observacoes_opcional(self):
        """Testa que observações é opcional"""
        item = ItemPedidoCreate(
            produto_id=1,
            quantidade=1
        )
        assert item.observacoes is None

        item_com_obs = ItemPedidoCreate(
            produto_id=1,
            quantidade=1,
            observacoes="Sem cebola"
        )
        assert item_com_obs.observacoes == "Sem cebola"


class TestPedidoSchema:
    """Testes do schema PedidoCreate"""

    def test_pedido_com_itens_valido(self):
        """Testa criação de pedido com itens"""
        pedido = PedidoCreate(
            itens=[
                ItemPedidoCreate(
                    produto_id=1,
                    quantidade=1
                )
            ]
        )
        assert len(pedido.itens) == 1
        assert pedido.itens[0].produto_id == 1
        assert pedido.itens[0].quantidade == 1

    def test_pedido_sem_itens(self):
        """Testa que pedido pode ser criado (lista vazia é o padrão)"""
        pedido = PedidoCreate()
        assert pedido.itens == []

    def test_pedido_multiplos_itens(self):
        """Testa pedido com múltiplos itens"""
        pedido = PedidoCreate(
            itens=[
                ItemPedidoCreate(produto_id=1, quantidade=2),
                ItemPedidoCreate(produto_id=2, quantidade=1),
            ]
        )
        assert len(pedido.itens) == 2
