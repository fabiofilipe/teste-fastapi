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
        assert "database" in data
        assert data["database"] == "connected"

    def test_metrics(self, client):
        """Testa endpoint de métricas"""
        response = client.get("/metrics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_usuarios" in data
        assert "total_produtos" in data
        assert "total_pedidos" in data
        assert isinstance(data["total_usuarios"], int)
        assert isinstance(data["total_produtos"], int)
        assert isinstance(data["total_pedidos"], int)

    def test_info(self, client):
        """Testa endpoint de informações da API"""
        response = client.get("/info")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "api_name" in data
        assert "version" in data
        assert "description" in data

    def test_status(self, client):
        """Testa endpoint de status combinado"""
        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "health" in data
        assert "metrics" in data
        assert "timestamp" in data
        assert data["health"]["status"] == "healthy"
