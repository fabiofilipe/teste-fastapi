"""Testes unitários para schemas Pydantic"""
import pytest
from pydantic import ValidationError
from app.schemas.schemas import (
    UsuarioSchema,
    UsuarioResponse,
    LoginSchema,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
    ItemPedidoCreate,
    PedidoCreate,
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaResponse,
    IngredienteCreate,
    IngredienteUpdate,
    IngredienteResponse,
    ProdutoVariacaoCreate,
    ProdutoVariacaoUpdate,
    ProdutoVariacaoResponse
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






class TestPedidoSchema:
    """Testes do schema PedidoCreate"""

    def test_pedido_com_itens_valido(self):
        """Testa criação de pedido com itens"""
        pedido = PedidoCreate(
            itens=[
                ItemPedidoCreate(
                    produto_variacao_id=1,
                    quantidade=1
                )
            ]
        )
        assert len(pedido.itens) == 1
        assert pedido.itens[0].produto_variacao_id == 1
        assert pedido.itens[0].quantidade == 1

    def test_pedido_sem_itens(self):
        """Testa que pedido pode ser criado (lista vazia é o padrão)"""
        pedido = PedidoCreate()
        assert pedido.itens == []

    def test_pedido_multiplos_itens(self):
        """Testa pedido com múltiplos itens"""
        pedido = PedidoCreate(
            itens=[
                ItemPedidoCreate(produto_variacao_id=1, quantidade=2),
                ItemPedidoCreate(produto_variacao_id=2, quantidade=1),
            ]
        )
        assert len(pedido.itens) == 2


class TestCategoriaSchema:
    """Testes dos schemas de Categoria"""

    def test_categoria_create_valida(self):
        """Testa criação de categoria válida"""
        categoria = CategoriaCreate(
            nome="Pizzas",
            descricao="Pizzas tradicionais e especiais",
            icone="🍕",
            ordem_exibicao=1,
            ativa=True
        )
        assert categoria.nome == "Pizzas"
        assert categoria.descricao == "Pizzas tradicionais e especiais"
        assert categoria.icone == "🍕"
        assert categoria.ordem_exibicao == 1
        assert categoria.ativa is True

    def test_categoria_nome_muito_curto(self):
        """Testa que nome deve ter no mínimo 3 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            CategoriaCreate(nome="Pi")
        assert "at least 3 characters" in str(exc_info.value)

    def test_categoria_campos_opcionais(self):
        """Testa campos opcionais de categoria"""
        categoria = CategoriaCreate(nome="Bebidas")
        assert categoria.descricao is None
        assert categoria.icone is None
        assert categoria.ordem_exibicao == 0
        assert categoria.ativa is True

    def test_categoria_ordem_exibicao_negativa(self):
        """Testa que ordem_exibicao não pode ser negativa"""
        with pytest.raises(ValidationError) as exc_info:
            CategoriaCreate(nome="Pizzas", ordem_exibicao=-1)
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_categoria_update_parcial(self):
        """Testa atualização parcial de categoria"""
        categoria_update = CategoriaUpdate(nome="Pizzas Especiais")
        assert categoria_update.nome == "Pizzas Especiais"
        assert categoria_update.descricao is None
        assert categoria_update.icone is None
        assert categoria_update.ordem_exibicao is None
        assert categoria_update.ativa is None


class TestIngredienteSchema:
    """Testes dos schemas de Ingrediente"""

    def test_ingrediente_create_valido(self):
        """Testa criação de ingrediente válido"""
        ingrediente = IngredienteCreate(
            nome="Mussarela",
            preco_adicional=0.0,
            disponivel=True
        )
        assert ingrediente.nome == "Mussarela"
        assert ingrediente.preco_adicional == 0.0
        assert ingrediente.disponivel is True

    def test_ingrediente_nome_muito_curto(self):
        """Testa que nome deve ter no mínimo 2 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            IngredienteCreate(nome="M")
        assert "at least 2 characters" in str(exc_info.value)

    def test_ingrediente_preco_negativo(self):
        """Testa que preço não pode ser negativo"""
        with pytest.raises(ValidationError) as exc_info:
            IngredienteCreate(nome="Tomate", preco_adicional=-1.0)
        assert "greater than or equal to 0" in str(exc_info.value)

    def test_ingrediente_campos_padrao(self):
        """Testa valores padrão de ingrediente"""
        ingrediente = IngredienteCreate(nome="Oregano")
        assert ingrediente.preco_adicional == 0.0
        assert ingrediente.disponivel is True

    def test_ingrediente_update_parcial(self):
        """Testa atualização parcial de ingrediente"""
        ing_update = IngredienteUpdate(preco_adicional=2.5)
        assert ing_update.nome is None
        assert ing_update.preco_adicional == 2.5
        assert ing_update.disponivel is None


class TestProdutoVariacaoSchema:
    """Testes dos schemas de ProdutoVariacao"""

    def test_variacao_create_valida(self):
        """Testa criação de variação válida"""
        variacao = ProdutoVariacaoCreate(
            tamanho="MEDIA",
            preco=35.00,
            disponivel=True
        )
        assert variacao.tamanho == "MEDIA"
        assert variacao.preco == 35.00
        assert variacao.disponivel is True

    def test_variacao_tamanhos_validos(self):
        """Testa que apenas tamanhos válidos são aceitos"""
        tamanhos_validos = ["PEQUENA", "MEDIA", "GRANDE", "GIGANTE", "UNICO"]

        for tamanho in tamanhos_validos:
            variacao = ProdutoVariacaoCreate(tamanho=tamanho, preco=30.00)
            assert variacao.tamanho == tamanho

    def test_variacao_tamanho_invalido(self):
        """Testa que tamanho inválido é rejeitado"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoVariacaoCreate(tamanho="ENORME", preco=30.00)
        assert "string should match pattern" in str(exc_info.value).lower()

    def test_variacao_preco_zero_invalido(self):
        """Testa que preço deve ser maior que zero"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoVariacaoCreate(tamanho="MEDIA", preco=0)
        assert "greater than 0" in str(exc_info.value)

    def test_variacao_preco_negativo_invalido(self):
        """Testa que preço não pode ser negativo"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoVariacaoCreate(tamanho="MEDIA", preco=-10.00)
        assert "greater than 0" in str(exc_info.value)

    def test_variacao_disponivel_padrao(self):
        """Testa valor padrão de disponivel"""
        variacao = ProdutoVariacaoCreate(tamanho="GRANDE", preco=45.00)
        assert variacao.disponivel is True

    def test_variacao_update_parcial(self):
        """Testa atualização parcial de variação"""
        var_update = ProdutoVariacaoUpdate(preco=40.00)
        assert var_update.tamanho is None
        assert var_update.preco == 40.00
        assert var_update.disponivel is None


class TestProdutoSchemaCompleto:
    """Testes completos dos schemas de Produto com variações"""

    def test_produto_create_com_variacoes(self):
        """Testa criação de produto com variações"""
        produto = ProdutoCreate(
            categoria_id=1,
            nome="Pizza Margherita",
            descricao="Molho, mussarela e manjericão",
            variacoes=[
                ProdutoVariacaoCreate(tamanho="PEQUENA", preco=25.00),
                ProdutoVariacaoCreate(tamanho="MEDIA", preco=35.00),
                ProdutoVariacaoCreate(tamanho="GRANDE", preco=45.00),
            ],
            ingredientes_ids=[1, 2, 3]
        )
        assert produto.categoria_id == 1
        assert produto.nome == "Pizza Margherita"
        assert len(produto.variacoes) == 3
        assert len(produto.ingredientes_ids) == 3

    def test_produto_create_sem_variacoes_invalido(self):
        """Testa que produto precisa ter pelo menos uma variação"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                categoria_id=1,
                nome="Pizza Margherita",
                variacoes=[]
            )
        assert "at least 1 item" in str(exc_info.value).lower()

    def test_produto_create_categoria_id_invalido(self):
        """Testa que categoria_id deve ser maior que zero"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                categoria_id=0,
                nome="Pizza Margherita",
                variacoes=[ProdutoVariacaoCreate(tamanho="MEDIA", preco=35.00)]
            )
        assert "greater than 0" in str(exc_info.value)

    def test_produto_create_nome_muito_curto(self):
        """Testa que nome deve ter no mínimo 3 caracteres"""
        with pytest.raises(ValidationError) as exc_info:
            ProdutoCreate(
                categoria_id=1,
                nome="Pi",
                variacoes=[ProdutoVariacaoCreate(tamanho="MEDIA", preco=35.00)]
            )
        assert "at least 3 characters" in str(exc_info.value)

    def test_produto_create_campos_opcionais(self):
        """Testa campos opcionais de produto"""
        produto = ProdutoCreate(
            categoria_id=1,
            nome="Pizza Simples",
            variacoes=[ProdutoVariacaoCreate(tamanho="MEDIA", preco=30.00)]
        )
        assert produto.descricao is None
        assert produto.imagem_url is None
        assert produto.disponivel is True
        assert produto.ingredientes_ids == []

    def test_produto_update_parcial(self):
        """Testa atualização parcial de produto"""
        produto_update = ProdutoUpdate(nome="Pizza Margherita Premium")
        assert produto_update.nome == "Pizza Margherita Premium"
        assert produto_update.categoria_id is None
        assert produto_update.descricao is None
        assert produto_update.disponivel is None


class TestItemPedidoSchemaCompleto:
    """Testes completos do schema ItemPedidoCreate atualizado"""

    def test_item_pedido_com_customizacoes(self):
        """Testa item de pedido com customizações de ingredientes"""
        item = ItemPedidoCreate(
            produto_variacao_id=1,
            quantidade=2,
            ingredientes_adicionados=[1, 2],
            ingredientes_removidos=[3],
            observacoes="Sem cebola"
        )
        assert item.produto_variacao_id == 1
        assert item.quantidade == 2
        assert item.ingredientes_adicionados == [1, 2]
        assert item.ingredientes_removidos == [3]
        assert item.observacoes == "Sem cebola"

    def test_item_pedido_minimo(self):
        """Testa item de pedido com campos mínimos"""
        item = ItemPedidoCreate(
            produto_variacao_id=1,
            quantidade=1
        )
        assert item.produto_variacao_id == 1
        assert item.quantidade == 1
        assert item.ingredientes_adicionados == []
        assert item.ingredientes_removidos == []
        assert item.observacoes is None

    def test_item_pedido_produto_variacao_id_invalido(self):
        """Testa que produto_variacao_id deve ser maior que zero"""
        with pytest.raises(ValidationError) as exc_info:
            ItemPedidoCreate(produto_variacao_id=0, quantidade=1)
        assert "greater than 0" in str(exc_info.value)
