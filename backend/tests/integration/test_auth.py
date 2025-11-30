"""Testes de integração para autenticação"""
import pytest
from fastapi import status


class TestAuthEndpoints:
    """Testes dos endpoints de autenticação"""

    def test_rota_inicial_auth(self, client):
        """Testa GET /auth/"""
        response = client.get("/auth/")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()

    def test_criar_conta_sucesso(self, client):
        """Testa criação de conta com sucesso"""
        response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Novo Usuario",
                "email": "novo@exemplo.com",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nome"] == "Novo Usuario"
        assert data["email"] == "novo@exemplo.com"
        assert "id" in data
        assert "senha" not in data
        assert data["ativo"] is True
        assert data["admin"] is False

    def test_criar_conta_email_duplicado(self, client, usuario_teste):
        """Testa que não é possível criar conta com email duplicado"""
        response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Outro Usuario",
                "email": usuario_teste.email,
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "já está cadastrado" in response.json()["message"]

    def test_criar_conta_email_invalido(self, client):
        """Testa validação de email inválido"""
        response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Usuario",
                "email": "email-invalido",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_criar_conta_senha_curta(self, client):
        """Testa validação de senha muito curta"""
        response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Usuario",
                "email": "usuario@exemplo.com",
                "senha": "123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_criar_conta_nome_curto(self, client):
        """Testa validação de nome muito curto"""
        response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Ab",
                "email": "usuario@exemplo.com",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLoginEndpoint:
    """Testes do endpoint de login"""

    def test_login_sucesso(self, client, usuario_teste):
        """Testa login com credenciais válidas"""
        response = client.post(
            "/auth/login",
            json={
                "email": "teste@exemplo.com",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"

    def test_login_email_inexistente(self, client):
        """Testa login com email que não existe"""
        response = client.post(
            "/auth/login",
            json={
                "email": "naoexiste@exemplo.com",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email ou senha incorretos" in response.json()["message"]

    def test_login_senha_incorreta(self, client, usuario_teste):
        """Testa login com senha incorreta"""
        response = client.post(
            "/auth/login",
            json={
                "email": "teste@exemplo.com",
                "senha": "senhaerrada"
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Email ou senha incorretos" in response.json()["message"]

    def test_login_usuario_inativo(self, client, db, usuario_teste):
        """Testa login com usuário inativo"""
        # Desativar usuário
        usuario_teste.ativo = False
        db.commit()

        response = client.post(
            "/auth/login",
            json={
                "email": "teste@exemplo.com",
                "senha": "senha123"
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "inativo" in response.json()["message"].lower()

    def test_login_campos_obrigatorios(self, client):
        """Testa que email e senha são obrigatórios"""
        response = client.post("/auth/login", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.post("/auth/login", json={"email": "teste@exemplo.com"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.post("/auth/login", json={"senha": "senha123"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRefreshTokenEndpoint:
    """Testes do endpoint de refresh token"""

    def test_refresh_token_sucesso(self, client, usuario_teste):
        """Testa renovação de token com refresh token válido"""
        # Fazer login para obter tokens
        login_response = client.post(
            "/auth/login",
            json={
                "email": "teste@exemplo.com",
                "senha": "senha123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]

        # Usar refresh token para obter novo access token
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "Bearer"

    def test_refresh_token_invalido(self, client):
        """Testa renovação com token inválido"""
        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "token_invalido_xyz"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_expirado(self, client):
        """Testa renovação com token expirado"""
        from jose import jwt
        from datetime import datetime, timedelta, timezone
        from app.config import SECRET_KEY, ALGORITHM

        # Criar token expirado
        data_expiracao = datetime.now(timezone.utc) - timedelta(days=1)
        claims = {"sub": "1", "exp": data_expiracao}
        token_expirado = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

        response = client.post(
            "/auth/refresh",
            json={"refresh_token": token_expirado}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_usuario_inexistente(self, client):
        """Testa renovação com token de usuário que não existe"""
        from jose import jwt
        from datetime import datetime, timedelta, timezone
        from app.config import SECRET_KEY, ALGORITHM

        # Criar token para usuário inexistente
        data_expiracao = datetime.now(timezone.utc) + timedelta(days=7)
        claims = {"sub": "99999", "exp": data_expiracao}
        token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)

        response = client.post(
            "/auth/refresh",
            json={"refresh_token": token}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticationFlow:
    """Testes de fluxo completo de autenticação"""

    def test_fluxo_completo_registro_login_refresh(self, client):
        """Testa fluxo completo: registro -> login -> refresh"""
        # 1. Criar conta
        registro_response = client.post(
            "/auth/criar_conta",
            json={
                "nome": "Usuario Fluxo",
                "email": "fluxo@exemplo.com",
                "senha": "senha123"
            }
        )
        assert registro_response.status_code == status.HTTP_201_CREATED
        usuario_id = registro_response.json()["id"]

        # 2. Fazer login
        login_response = client.post(
            "/auth/login",
            json={
                "email": "fluxo@exemplo.com",
                "senha": "senha123"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        tokens = login_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        # 3. Usar access token em endpoint protegido (exemplo: listar produtos)
        headers = {"Authorization": f"Bearer {access_token}"}
        produtos_response = client.get("/produtos/", headers=headers)
        assert produtos_response.status_code == status.HTTP_200_OK

        # 4. Renovar token
        refresh_response = client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        new_tokens = refresh_response.json()
        new_access_token = new_tokens["access_token"]

        # 5. Usar novo access token
        headers = {"Authorization": f"Bearer {new_access_token}"}
        produtos_response2 = client.get("/produtos/", headers=headers)
        assert produtos_response2.status_code == status.HTTP_200_OK

    def test_token_contem_usuario_id_correto(self, client, usuario_teste):
        """Testa que token JWT contém o ID correto do usuário"""
        from jose import jwt
        from app.config import SECRET_KEY, ALGORITHM

        # Fazer login
        response = client.post(
            "/auth/login",
            json={
                "email": "teste@exemplo.com",
                "senha": "senha123"
            }
        )
        access_token = response.json()["access_token"]

        # Decodificar token e verificar claims
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == str(usuario_teste.id)
        assert "exp" in payload
