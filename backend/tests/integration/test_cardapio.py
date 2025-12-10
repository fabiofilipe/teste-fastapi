"""Testes de integração para o router de cardápio"""
import pytest
from fastapi import status


class TestCardapioCompleto:
    """Testes para listagem do cardápio completo"""

    def test_listar_cardapio_completo(self, client, cardapio_completo):
        """Deve retornar cardápio completo com categorias e produtos"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "categorias" in data
        assert len(data["categorias"]) == 3  # Apenas ativas

    def test_cardapio_apenas_categorias_ativas(self, client, cardapio_completo):
        """Cardápio deve incluir apenas categorias ativas"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        categorias = data["categorias"]
        assert all(cat["ativa"] for cat in categorias)

    def test_cardapio_categorias_ordenadas(self, client, cardapio_completo):
        """Categorias devem vir ordenadas por ordem_exibicao"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        categorias = data["categorias"]
        ordens = [cat["ordem_exibicao"] for cat in categorias]
        assert ordens == sorted(ordens)

    def test_cardapio_apenas_produtos_disponiveis(self, client, cardapio_completo):
        """Cardápio deve incluir apenas produtos disponíveis"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verificar que todos os produtos são disponíveis
        for categoria in data["categorias"]:
            for produto in categoria["produtos"]:
                assert produto["disponivel"] is True

    def test_cardapio_produtos_com_variacoes(self, client, cardapio_completo):
        """Produtos no cardápio devem incluir variações"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verificar que produtos têm variações
        categoria_pizza = data["categorias"][0]
        if categoria_pizza["produtos"]:
            produto = categoria_pizza["produtos"][0]
            assert "variacoes" in produto
            assert len(produto["variacoes"]) > 0

    def test_cardapio_produtos_com_ingredientes(self, client, cardapio_completo):
        """Produtos no cardápio devem incluir ingredientes"""
        response = client.get("/cardapio/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verificar que produtos têm ingredientes
        categoria_pizza = data["categorias"][0]
        if categoria_pizza["produtos"]:
            produto = categoria_pizza["produtos"][0]
            assert "ingredientes" in produto


class TestProdutosPorCategoria:
    """Testes para listagem de produtos por categoria"""

    def test_listar_produtos_de_categoria(self, client, cardapio_completo):
        """Deve listar produtos de uma categoria específica"""
        categorias = cardapio_completo["categorias"]
        categoria_id = categorias[0].id

        response = client.get(f"/cardapio/categorias/{categoria_id}/produtos")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # Verificar que todos os produtos pertencem à categoria
        for produto in data:
            assert produto["categoria_id"] == categoria_id

    def test_listar_produtos_categoria_sem_produtos(self, client, categoria_teste):
        """Categoria sem produtos deve retornar lista vazia"""
        response = client.get(f"/cardapio/categorias/{categoria_teste.id}/produtos")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_incluir_produtos_indisponiveis(self, client, cardapio_completo):
        """Com incluir_indisponiveis=True deve mostrar produtos indisponíveis"""
        categorias = cardapio_completo["categorias"]
        categoria_sobremesa = categorias[2]

        response = client.get(
            f"/cardapio/categorias/{categoria_sobremesa.id}/produtos?incluir_indisponiveis=true"
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Deve incluir o Brownie que está indisponível
        assert len(data) >= 1


class TestBuscaProdutos:
    """Testes para busca de produtos"""

    def test_buscar_produtos_por_nome(self, client, cardapio_completo):
        """Deve encontrar produtos pelo nome"""
        response = client.get("/cardapio/buscar?termo=Pizza")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0
        # Verificar que todos contêm "Pizza" no nome
        assert all("pizza" in produto["nome"].lower() for produto in data)

    def test_buscar_produtos_por_descricao(self, client, cardapio_completo):
        """Deve encontrar produtos pela descrição"""
        response = client.get("/cardapio/buscar?termo=Calabresa")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) > 0

    def test_buscar_produtos_case_insensitive(self, client, cardapio_completo):
        """Busca deve ser case-insensitive"""
        response1 = client.get("/cardapio/buscar?termo=pizza")
        response2 = client.get("/cardapio/buscar?termo=PIZZA")

        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK

        data1 = response1.json()
        data2 = response2.json()

        # Devem retornar os mesmos resultados
        assert len(data1) == len(data2)

    def test_buscar_produtos_termo_minimo(self, client):
        """Busca deve exigir mínimo de 2 caracteres"""
        response = client.get("/cardapio/buscar?termo=P")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_buscar_apenas_produtos_disponiveis(self, client, cardapio_completo):
        """Busca deve retornar apenas produtos disponíveis"""
        response = client.get("/cardapio/buscar?termo=a")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Todos os produtos devem estar disponíveis
        for produto in data:
            assert produto["disponivel"] is True

    def test_buscar_produtos_sem_resultados(self, client, cardapio_completo):
        """Busca sem resultados deve retornar lista vazia"""
        response = client.get("/cardapio/buscar?termo=XYZABC123")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []
