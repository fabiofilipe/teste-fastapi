"""Testes de integração para produtos"""
import pytest
from fastapi import status


class TestCreateProduct:
    """Testes de criação de produtos"""

    def test_criar_produto_como_admin(self, client, token_admin):
        """Testa criação de produto por admin"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.post(
            "/produtos/",
            headers=headers,
            json={
                "nome": "Pizza Margherita",
                "descricao": "Molho, mussarela e manjericão",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 35.00
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nome"] == "Pizza Margherita"
        assert data["categoria"] == "PIZZA"
        assert data["tamanho"] == "MEDIA"
        assert data["preco"] == 35.00
        assert data["disponivel"] is True

    def test_criar_produto_sem_autenticacao(self, client):
        """Testa que criar produto requer autenticação"""
        response = client.post(
            "/produtos/",
            json={
                "nome": "Pizza Margherita",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 35.00
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_produto_usuario_comum(self, client, token_usuario):
        """Testa que usuário comum não pode criar produto"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.post(
            "/produtos/",
            headers=headers,
            json={
                "nome": "Pizza Margherita",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 35.00
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_produto_duplicado(self, client, token_admin, produto_teste):
        """Testa que não pode criar produto duplicado (mesmo nome e tamanho)"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.post(
            "/produtos/",
            headers=headers,
            json={
                "nome": produto_teste.nome,
                "categoria": "PIZZA",
                "tamanho": produto_teste.tamanho,
                "preco": 40.00
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "já existe" in response.json()["message"]


class TestListProducts:
    """Testes de listagem de produtos"""

    def test_listar_produtos(self, client, produtos_diversos):
        """Testa listagem de todos os produtos"""
        response = client.get("/produtos/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(produtos_diversos)

    def test_listar_produtos_disponiveis(self, client, produtos_diversos):
        """Testa filtro por produtos disponíveis"""
        response = client.get("/produtos/?disponivel=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(produto["disponivel"] is True for produto in data)

    def test_listar_produtos_indisponiveis(self, client, produtos_diversos):
        """Testa filtro por produtos indisponíveis"""
        response = client.get("/produtos/?disponivel=false")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(produto["disponivel"] is False for produto in data)

    def test_listar_produtos_por_categoria(self, client, produtos_diversos):
        """Testa filtro por categoria"""
        response = client.get("/produtos/?categoria=PIZZA")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(produto["categoria"] == "PIZZA" for produto in data)

        response = client.get("/produtos/?categoria=BEBIDA")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(produto["categoria"] == "BEBIDA" for produto in data)

    def test_listar_produtos_filtros_combinados(self, client, produtos_diversos):
        """Testa filtros combinados"""
        response = client.get("/produtos/?categoria=PIZZA&disponivel=true")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(
            produto["categoria"] == "PIZZA" and produto["disponivel"] is True
            for produto in data
        )


class TestGetProduct:
    """Testes de busca de produto específico"""

    def test_buscar_produto_existente(self, client, produto_teste):
        """Testa busca de produto por ID"""
        response = client.get(f"/produtos/{produto_teste.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == produto_teste.id
        assert data["nome"] == produto_teste.nome

    def test_buscar_produto_inexistente(self, client):
        """Testa busca de produto que não existe"""
        response = client.get("/produtos/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "não encontrado" in response.json()["message"]


class TestUpdateProduct:
    """Testes de atualização de produtos"""

    def test_atualizar_produto_como_admin(self, client, token_admin, produto_teste):
        """Testa atualização de produto por admin"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.put(
            f"/produtos/{produto_teste.id}",
            headers=headers,
            json={
                "nome": "Pizza Margherita Premium",
                "descricao": "Agora com mussarela de búfala",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 45.00
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nome"] == "Pizza Margherita Premium"
        assert data["preco"] == 45.00
        assert data["descricao"] == "Agora com mussarela de búfala"

    def test_atualizar_produto_sem_autenticacao(self, client, produto_teste):
        """Testa que atualizar produto requer autenticação"""
        response = client.put(
            f"/produtos/{produto_teste.id}",
            json={
                "nome": "Pizza Margherita Premium",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 45.00
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_atualizar_produto_usuario_comum(self, client, token_usuario, produto_teste):
        """Testa que usuário comum não pode atualizar produto"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.put(
            f"/produtos/{produto_teste.id}",
            headers=headers,
            json={
                "nome": "Pizza Margherita Premium",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 45.00
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_atualizar_produto_inexistente(self, client, token_admin):
        """Testa atualização de produto que não existe"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.put(
            "/produtos/99999",
            headers=headers,
            json={
                "nome": "Pizza Margherita",
                "categoria": "PIZZA",
                "tamanho": "MEDIA",
                "preco": 35.00
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteProduct:
    """Testes de exclusão de produtos"""

    def test_deletar_produto_como_admin(self, client, token_admin, produto_teste):
        """Testa exclusão de produto por admin"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.delete(f"/produtos/{produto_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que produto foi deletado
        response = client.get(f"/produtos/{produto_teste.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deletar_produto_sem_autenticacao(self, client, produto_teste):
        """Testa que deletar produto requer autenticação"""
        response = client.delete(f"/produtos/{produto_teste.id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deletar_produto_usuario_comum(self, client, token_usuario, produto_teste):
        """Testa que usuário comum não pode deletar produto"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.delete(f"/produtos/{produto_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_deletar_produto_inexistente(self, client, token_admin):
        """Testa exclusão de produto que não existe"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.delete("/produtos/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateProductAvailability:
    """Testes de atualização de disponibilidade"""

    def test_alterar_disponibilidade_como_admin(self, client, token_admin, produto_teste):
        """Testa alteração de disponibilidade por admin"""
        headers = {"Authorization": f"Bearer {token_admin}"}

        # Tornar indisponível
        response = client.patch(
            f"/produtos/{produto_teste.id}/disponibilidade",
            headers=headers,
            params={"disponivel": False}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["disponivel"] is False

        # Tornar disponível novamente
        response = client.patch(
            f"/produtos/{produto_teste.id}/disponibilidade",
            headers=headers,
            params={"disponivel": True}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["disponivel"] is True

    def test_alterar_disponibilidade_sem_autenticacao(self, client, produto_teste):
        """Testa que alterar disponibilidade requer autenticação"""
        response = client.patch(
            f"/produtos/{produto_teste.id}/disponibilidade",
            params={"disponivel": False}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_alterar_disponibilidade_usuario_comum(self, client, token_usuario, produto_teste):
        """Testa que usuário comum não pode alterar disponibilidade"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.patch(
            f"/produtos/{produto_teste.id}/disponibilidade",
            headers=headers,
            params={"disponivel": False}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
