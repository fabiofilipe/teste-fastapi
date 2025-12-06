"""Testes de integração para health checks"""
from fastapi import status


class TestHealthEndpoints:
    """Testes dos endpoints de saúde"""

    def test_health_check(self, client):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data
        assert data["services"]["database"]["status"] == "healthy"

    def test_metrics(self, client):
        """Testa endpoint de métricas"""
        response = client.get("/metrics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "usuarios" in data
        assert "produtos" in data
        assert "pedidos" in data
        assert isinstance(data["usuarios"]["total"], int)
        assert isinstance(data["produtos"]["total"], int)
        assert isinstance(data["pedidos"]["total"], int)

    def test_info(self, client):
        """Testa endpoint de informações da API"""
        response = client.get("/info")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "description" in data

    def test_status(self, client):
        """Testa endpoint de status combinado"""
        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert data["status"] == "operational"

