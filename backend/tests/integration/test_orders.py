"""Testes de integração para pedidos"""
import pytest
from fastapi import status


class TestCreateOrder:
    """Testes de criação de pedidos"""

    def test_criar_pedido_sucesso(self, client, token_usuario, produto_teste):
        """Testa criação de pedido com sucesso"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.post(
            "/pedidos/",
            headers=headers,
            json={
                "itens": [
                    {
                        "produto_id": produto_teste.id,
                        "quantidade": 2
                    }
                ]
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "PENDENTE"
        assert len(data["itens"]) == 1
        assert data["preco_total"] == produto_teste.preco * 2

    def test_criar_pedido_sem_autenticacao(self, client, produto_teste):
        """Testa que criar pedido requer autenticação"""
        response = client.post(
            "/pedidos/",
            json={
                "itens": [
                    {
                        "produto_id": produto_teste.id,
                        "quantidade": 1
                    }
                ]
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_criar_pedido_sem_itens(self, client, token_usuario):
        """Testa que pedido deve ter pelo menos 1 item"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.post(
            "/pedidos/",
            headers=headers,
            json={"itens": []}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_criar_pedido_produto_indisponivel(self, client, token_usuario, db, produtos_diversos):
        """Testa que não pode criar pedido com produto indisponível"""
        # produtos_diversos[3] é o Brownie que está indisponível
        produto_indisponivel = produtos_diversos[3]

        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.post(
            "/pedidos/",
            headers=headers,
            json={
                "itens": [
                    {
                        "produto_id": produto_indisponivel.id,
                        "quantidade": 1
                    }
                ]
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "não está disponível" in response.json()["message"]


class TestCalculatePrice:
    """Testes de cálculo de preço"""

    def test_calcular_preco_sucesso(self, client, token_usuario, produto_teste):
        """Testa cálculo de preço antes de criar pedido"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.post(
            "/pedidos/calcular-preco",
            headers=headers,
            json={
                "itens": [
                    {
                        "produto_id": produto_teste.id,
                        "quantidade": 2
                    }
                ]
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["preco_calculado"] == produto_teste.preco * 2
        assert len(data["itens"]) == 1


class TestListMyOrders:
    """Testes de listagem de pedidos do usuário"""

    def test_listar_meus_pedidos(self, client, token_usuario, pedido_teste):
        """Testa listagem de pedidos do próprio usuário"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get("/pedidos/meus", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_listar_meus_pedidos_filtro_status(self, client, token_usuario, pedido_teste):
        """Testa filtro por status nos meus pedidos"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get("/pedidos/meus?status=PENDENTE", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(pedido["status"] == "PENDENTE" for pedido in data)

    def test_listar_meus_pedidos_sem_autenticacao(self, client):
        """Testa que listar pedidos requer autenticação"""
        response = client.get("/pedidos/meus")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_usuario_ve_apenas_seus_pedidos(self, client, db, usuario_teste, admin_teste, produto_teste):
        """Testa que usuário vê apenas seus próprios pedidos"""
        from app.models.models import Pedido, ItemPedido

        # Criar pedido para usuário
        pedido_usuario = Pedido(usuario_id=usuario_teste.id, status="PENDENTE", preco_total=35.00)
        db.add(pedido_usuario)
        db.commit()

        # Criar pedido para admin
        pedido_admin = Pedido(usuario_id=admin_teste.id, status="PENDENTE", preco_total=50.00)
        db.add(pedido_admin)
        db.commit()

        # Login como usuário
        login_response = client.post(
            "/auth/login",
            json={"email": "teste@exemplo.com", "senha": "senha123"}
        )
        token = login_response.json()["access_token"]

        # Listar pedidos do usuário
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/pedidos/meus", headers=headers)
        data = response.json()

        # Verificar que só vê seus pedidos
        assert all(pedido["usuario_id"] == usuario_teste.id for pedido in data)
        assert not any(pedido["usuario_id"] == admin_teste.id for pedido in data)


class TestListAllOrders:
    """Testes de listagem de todos os pedidos (admin)"""

    def test_listar_todos_pedidos_como_admin(self, client, token_admin, pedido_teste):
        """Testa que admin pode listar todos os pedidos"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.get("/pedidos/", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    def test_listar_todos_pedidos_usuario_comum(self, client, token_usuario):
        """Testa que usuário comum não pode listar todos os pedidos"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get("/pedidos/", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestGetOrder:
    """Testes de busca de pedido específico"""

    def test_buscar_pedido_proprio(self, client, token_usuario, pedido_teste):
        """Testa busca do próprio pedido"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get(f"/pedidos/{pedido_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == pedido_teste.id

    def test_buscar_pedido_de_outro_usuario(self, client, db, admin_teste, usuario_teste, produto_teste):
        """Testa que não pode buscar pedido de outro usuário"""
        from app.models.models import Pedido

        # Criar pedido para admin
        pedido_admin = Pedido(usuario_id=admin_teste.id, status="PENDENTE", preco_total=50.00)
        db.add(pedido_admin)
        db.commit()
        db.refresh(pedido_admin)

        # Login como usuário comum
        login_response = client.post(
            "/auth/login",
            json={"email": usuario_teste.email, "senha": "senha123"}
        )
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(f"/pedidos/{pedido_admin.id}", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_buscar_qualquer_pedido(self, client, token_admin, pedido_teste):
        """Testa que admin pode buscar qualquer pedido"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.get(f"/pedidos/{pedido_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK

    def test_buscar_pedido_inexistente(self, client, token_usuario):
        """Testa busca de pedido que não existe"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get("/pedidos/99999", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateOrderStatus:
    """Testes de atualização de status de pedido"""

    def test_atualizar_status_como_admin(self, client, token_admin, pedido_teste):
        """Testa atualização de status por admin"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.patch(
            f"/pedidos/{pedido_teste.id}/status",
            headers=headers,
            params={"novo_status": "EM_PREPARO"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "EM_PREPARO"

    def test_atualizar_status_usuario_comum(self, client, token_usuario, pedido_teste):
        """Testa que usuário comum não pode atualizar status"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.patch(
            f"/pedidos/{pedido_teste.id}/status",
            headers=headers,
            params={"novo_status": "EM_PREPARO"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_atualizar_status_invalido(self, client, token_admin, pedido_teste):
        """Testa que não aceita status inválido"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.patch(
            f"/pedidos/{pedido_teste.id}/status",
            headers=headers,
            params={"novo_status": "STATUS_INVALIDO"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteOrder:
    """Testes de cancelamento de pedido"""

    def test_cancelar_pedido_proprio(self, client, token_usuario, pedido_teste):
        """Testa cancelamento do próprio pedido"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.delete(f"/pedidos/{pedido_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que pedido foi deletado
        response = client.get(f"/pedidos/{pedido_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancelar_pedido_de_outro_usuario(self, client, db, admin_teste, usuario_teste):
        """Testa que não pode cancelar pedido de outro usuário"""
        from app.models.models import Pedido

        # Criar pedido para admin
        pedido_admin = Pedido(usuario_id=admin_teste.id, status="PENDENTE", preco_total=50.00)
        db.add(pedido_admin)
        db.commit()
        db.refresh(pedido_admin)

        # Login como usuário comum
        login_response = client.post(
            "/auth/login",
            json={"email": usuario_teste.email, "senha": "senha123"}
        )
        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        response = client.delete(f"/pedidos/{pedido_admin.id}", headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_cancelar_qualquer_pedido(self, client, token_admin, pedido_teste):
        """Testa que admin pode cancelar qualquer pedido"""
        headers = {"Authorization": f"Bearer {token_admin}"}
        response = client.delete(f"/pedidos/{pedido_teste.id}", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestOrderStatistics:
    """Testes de estatísticas de pedidos"""

    def test_obter_estatisticas(self, client, token_usuario, pedido_teste):
        """Testa obtenção de estatísticas dos pedidos"""
        headers = {"Authorization": f"Bearer {token_usuario}"}
        response = client.get("/pedidos/meus/estatisticas", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_pedidos" in data
        assert "total_gasto" in data
        assert "pedidos_por_status" in data
