"""Factories para geração de dados de teste"""
import factory
from factory import Faker
import bcrypt

from app.models.models import (
    Usuario, Produto, Pedido, ItemPedido,
    Categoria, Ingrediente, ProdutoVariacao, ProdutoIngrediente
)


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


class CategoriaFactory(factory.Factory):
    """Factory para criar categorias de teste"""
    class Meta:
        model = Categoria

    nome = Faker("word")
    descricao = Faker("sentence")
    icone = "🍕"
    ordem_exibicao = 1
    ativa = True


class IngredienteFactory(factory.Factory):
    """Factory para criar ingredientes de teste"""
    class Meta:
        model = Ingrediente

    nome = Faker("word")
    preco_adicional = Faker("pyfloat", left_digits=1, right_digits=2, positive=True, min_value=0, max_value=10)
    disponivel = True


class ProdutoFactory(factory.Factory):
    """Factory para criar produtos de teste"""
    class Meta:
        model = Produto

    nome = Faker("word")
    descricao = Faker("sentence")
    imagem_url = Faker("image_url")
    disponivel = True
    # categoria_id deve ser fornecido ao criar


class ProdutoVariacaoFactory(factory.Factory):
    """Factory para criar variações de produto de teste"""
    class Meta:
        model = ProdutoVariacao

    tamanho = "MEDIA"
    preco = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=10, max_value=100)
    disponivel = True
    # produto_id deve ser fornecido ao criar


class ProdutoIngredienteFactory(factory.Factory):
    """Factory para criar associação produto-ingrediente de teste"""
    class Meta:
        model = ProdutoIngrediente

    quantidade = 1
    obrigatorio = False
    # produto_id e ingrediente_id devem ser fornecidos ao criar


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
    produto_nome = Faker("word")
    tamanho = "MEDIA"
    preco_base = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=10, max_value=100)
    ingredientes_adicionados = []
    ingredientes_removidos = []
    preco_ingredientes = 0.0
    preco_total = Faker("pyfloat", left_digits=2, right_digits=2, positive=True, min_value=10, max_value=100)
    observacoes = Faker("sentence")
    # pedido_id e produto_variacao_id devem ser fornecidos ao criar
