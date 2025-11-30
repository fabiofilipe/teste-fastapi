"""Factories para geração de dados de teste"""
import factory
from factory import Faker
import bcrypt

from app.models.models import Usuario, Produto, Pedido, ItemPedido


class UsuarioFactory(factory.Factory):
    """Factory para criar usuários de teste"""
    class Meta:
        model = Usuario

    nome = Faker("name", locale="pt_BR")
    email = Faker("email")
    ativo = True
    admin = False

    @factory.lazy_attribute
    def senha(self):
        """Gera hash bcrypt da senha padrão"""
        return bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()).decode()


class AdminFactory(UsuarioFactory):
    """Factory para criar usuários admin"""
    admin = True
    nome = "Admin"
    email = Faker("email")


class ProdutoFactory(factory.Factory):
    """Factory para criar produtos de teste"""
    class Meta:
        model = Produto

    nome = Faker("word")
    descricao = Faker("sentence")
    categoria = "PIZZA"
    tamanho = "MEDIA"
    preco = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=10, max_value=100)
    disponivel = True


class PedidoFactory(factory.Factory):
    """Factory para criar pedidos de teste"""
    class Meta:
        model = Pedido

    status = "PENDENTE"
    preco_total = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=20, max_value=200)


class ItemPedidoFactory(factory.Factory):
    """Factory para criar itens de pedido de teste"""
    class Meta:
        model = ItemPedido

    quantidade = 1
    sabor = Faker("word")
    tamanho = "MEDIA"
    preco_unitario = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=10, max_value=100)
    observacoes = Faker("sentence")
