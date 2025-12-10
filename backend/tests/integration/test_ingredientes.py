"""Testes de integração para o router de ingredientes"""
import pytest
from fastapi import status


class TestCreateIngrediente:
    """Testes para criação de ingredientes"""

    def test_criar_ingrediente_com_admin(self, client, token_admin):
        """Admin deve conseguir criar ingrediente"""
        response = client.post(
            "/ingredientes/",
            json={
                "nome": "Parmesão",
                "preco_adicional": 2.5,
                "disponivel": True
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nome"] == "Parmesão"
        assert data["preco_adicional"] == 2.5
        assert data["disponivel"] is True
        assert "id" in data

    def test_criar_ingrediente_sem_autenticacao(self, client):
        """Deve retornar 401 sem autenticação"""
        response = client.post(
            "/ingredientes/",
            json={
                "nome": "Parmesão",
                "preco_adicional": 2.5
            }
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_ingrediente_com_usuario_comum(self, client, token_usuario):
        """Usuário comum não deve conseguir criar ingrediente"""
        response = client.post(
            "/ingredientes/",
            json={
                "nome": "Parmesão",
                "preco_adicional": 2.5
            },
            headers={"Authorization": f"Bearer {token_usuario}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_ingrediente_preco_padrao_zero(self, client, token_admin):
        """Preco_adicional deve ter padrão 0.0"""
        response = client.post(
            "/ingredientes/",
            json={
                "nome": "Orégano"
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["preco_adicional"] == 0.0


class TestListIngredientes:
    """Testes para listagem de ingredientes"""

    def test_listar_todos_ingredientes(self, client, ingredientes_diversos):
        """Deve listar todos os ingredientes sem filtro"""
        response = client.get("/ingredientes/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 5  # Todos os ingredientes

    def test_listar_apenas_ingredientes_disponiveis(self, client, ingredientes_diversos):
        """Com apenas_disponiveis=True deve listar apenas disponíveis"""
        response = client.get("/ingredientes/?apenas_disponiveis=true")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 4  # 4 disponíveis (Bacon está indisponível)
        assert all(ing["disponivel"] for ing in data)

    def test_ingredientes_ordenados_por_nome(self, client, ingredientes_diversos):
        """Ingredientes devem vir ordenados por nome"""
        response = client.get("/ingredientes/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verificar ordem alfabética
        nomes = [ing["nome"] for ing in data]
        assert nomes == sorted(nomes)


class TestBuscarIngrediente:
    """Testes para buscar ingrediente por ID"""

    def test_buscar_ingrediente_existente(self, client, ingrediente_teste):
        """Deve retornar ingrediente existente"""
        response = client.get(f"/ingredientes/{ingrediente_teste.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == ingrediente_teste.id
        assert data["nome"] == ingrediente_teste.nome

    def test_buscar_ingrediente_inexistente(self, client):
        """Deve retornar 404 para ingrediente inexistente"""
        response = client.get("/ingredientes/99999")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateIngrediente:
    """Testes para atualização de ingrediente"""

    def test_atualizar_ingrediente_com_admin(self, client, token_admin, ingrediente_teste):
        """Admin deve conseguir atualizar ingrediente"""
        response = client.put(
            f"/ingredientes/{ingrediente_teste.id}",
            json={
                "nome": "Mussarela Premium",
                "preco_adicional": 3.0
            },
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nome"] == "Mussarela Premium"
        assert data["preco_adicional"] == 3.0

    def test_atualizar_ingrediente_sem_autenticacao(self, client, ingrediente_teste):
        """Deve retornar 401 sem autenticação"""
        response = client.put(
            f"/ingredientes/{ingrediente_teste.id}",
            json={"nome": "Novo Nome"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_atualizar_ingrediente_inexistente(self, client, token_admin):
        """Deve retornar 404 para ingrediente inexistente"""
        response = client.put(
            "/ingredientes/99999",
            json={"nome": "Teste"},
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAlternarDisponibilidadeIngrediente:
    """Testes para alternar disponibilidade de ingrediente"""

    def test_alternar_disponibilidade_com_admin(self, client, token_admin, ingrediente_teste):
        """Admin deve conseguir alternar disponibilidade"""
        disponibilidade_inicial = ingrediente_teste.disponivel

        response = client.patch(
            f"/ingredientes/{ingrediente_teste.id}/disponibilidade",
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["disponivel"] != disponibilidade_inicial

    def test_alternar_disponibilidade_sem_autenticacao(self, client, ingrediente_teste):
        """Deve retornar 401 sem autenticação"""
        response = client.patch(f"/ingredientes/{ingrediente_teste.id}/disponibilidade")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_alternar_disponibilidade_ingrediente_inexistente(self, client, token_admin):
        """Deve retornar 404 para ingrediente inexistente"""
        response = client.patch(
            "/ingredientes/99999/disponibilidade",
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteIngrediente:
    """Testes para deleção de ingrediente"""

    def test_deletar_ingrediente_com_admin(self, client, token_admin, ingrediente_teste):
        """Admin deve conseguir deletar ingrediente"""
        response = client.delete(
            f"/ingredientes/{ingrediente_teste.id}",
            headers={"Authorization": f"Bearer {token_admin}"}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que foi deletado
        response = client.get(f"/ingredientes/{ingrediente_teste.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deletar_ingrediente_sem_autenticacao(self, client, ingrediente_teste):
        """Deve retornar 401 sem autenticação"""
        response = client.delete(f"/ingredientes/{ingrediente_teste.id}")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deletar_ingrediente_com_usuario_comum(self, client, token_usuario, ingrediente_teste):
        """Usuário comum não deve conseguir deletar ingrediente"""
        response = client.delete(
            f"/ingredientes/{ingrediente_teste.id}",
            headers={"Authorization": f"Bearer {token_usuario}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
