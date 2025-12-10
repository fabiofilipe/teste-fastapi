"""Testes de integração para o router de categorias"""
import pytest
from fastapi import status


class TestCreateCategoria:
    """Testes para criação de categorias"""

    def test_criar_categoria_com_admin(self, client, token_admin):
        """Admin deve conseguir criar categoria"""
        response = client.post(
            "/categorias/",
            json={
                "nome": "Massas",
                "descricao": "Massas italianas",
                "icone": "🍝",
                "ordem_exibicao": 1,
                "ativa": True
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nome"] == "Massas"
        assert data["descricao"] == "Massas italianas"
        assert data["icone"] == "🍝"
        assert data["ordem_exibicao"] == 1
        assert data["ativa"] is True
        assert "id" in data
        assert "created_at" in data

    def test_criar_categoria_sem_autenticacao(self, client):
        """Deve retornar 403 sem autenticação"""
        response = client.post(
            "/categorias/",
            json={
                "nome": "Massas",
                "descricao": "Massas italianas"
            }
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_categoria_com_usuario_comum(self, client, token_usuario):
        """Usuário comum não deve conseguir criar categoria"""
        response = client.post(
            "/categorias/",
            json={
                "nome": "Massas",
                "descricao": "Massas italianas"
            },
            headers={"Authorization": f"Bearer {token_usuario}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_categoria_nome_duplicado(self, client, token_admin, categoria_teste):
        """Não deve permitir criar categoria com nome duplicado"""
        response = client.post(
            "/categorias/",
            json={
                "nome": categoria_teste.nome,
                "descricao": "Outra descrição"
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data or "message" in data


class TestListCategorias:
    """Testes para listagem de categorias"""

    def test_listar_apenas_categorias_ativas_por_padrao(self, client, categorias_diversas):
        """Por padrão deve listar apenas categorias ativas"""
        response = client.get("/categorias/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3  # 3 ativas
        assert all(cat["ativa"] for cat in data)

    def test_listar_todas_categorias_incluindo_inativas(self, client, categorias_diversas):
        """Com apenas_ativas=False deve retornar todas"""
        response = client.get("/categorias/?apenas_ativas=false")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 4  # Todas (3 ativas + 1 inativa)

    def test_categorias_ordenadas_por_ordem_exibicao(self, client, categorias_diversas):
        """Categorias devem vir ordenadas por ordem_exibicao"""
        response = client.get("/categorias/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verificar ordem crescente
        for i in range(len(data) - 1):
            assert data[i]["ordem_exibicao"] <= data[i + 1]["ordem_exibicao"]


class TestBuscarCategoria:
    """Testes para buscar categoria por ID"""

    def test_buscar_categoria_existente(self, client, categoria_teste):
        """Deve retornar categoria existente"""
        response = client.get(f"/categorias/{categoria_teste.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == categoria_teste.id
        assert data["nome"] == categoria_teste.nome

    def test_buscar_categoria_inexistente(self, client):
        """Deve retornar 404 para categoria inexistente"""
        response = client.get("/categorias/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateCategoria:
    """Testes para atualização de categoria"""

    def test_atualizar_categoria_com_admin(self, client, token_admin, categoria_teste):
        """Admin deve conseguir atualizar categoria"""
        response = client.put(
            f"/categorias/{categoria_teste.id}",
            json={
                "nome": "Pizzas Especiais",
                "ordem_exibicao": 10
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nome"] == "Pizzas Especiais"
        assert data["ordem_exibicao"] == 10

    def test_atualizar_categoria_sem_autenticacao(self, client, categoria_teste):
        """Deve retornar 403 sem autenticação"""
        response = client.put(
            f"/categorias/{categoria_teste.id}",
            json={"nome": "Novo Nome"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_atualizar_categoria_inexistente(self, client, token_admin):
        """Deve retornar 404 para categoria inexistente"""
        response = client.put(
            "/categorias/99999",
            json={"nome": "Teste"},
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteCategoria:
    """Testes para deleção de categoria"""

    def test_deletar_categoria_com_admin(self, client, token_admin, categoria_teste):
        """Admin deve conseguir deletar categoria"""
        response = client.delete(
            f"/categorias/{categoria_teste.id}",
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que foi deletada
        response = client.get(f"/categorias/{categoria_teste.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deletar_categoria_sem_autenticacao(self, client, categoria_teste):
        """Deve retornar 403 sem autenticação"""
        response = client.delete(f"/categorias/{categoria_teste.id}")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deletar_categoria_com_usuario_comum(self, client, token_usuario, categoria_teste):
        """Usuário comum não deve conseguir deletar categoria"""
        response = client.delete(
            f"/categorias/{categoria_teste.id}",
            headers={"Authorization": f"Bearer {token_usuario}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
