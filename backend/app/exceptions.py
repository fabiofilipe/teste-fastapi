"""Exceções customizadas para a aplicação"""
from fastapi import HTTPException, status


class PizzariaException(Exception):
    """Exceção base para erros da pizzaria"""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UsuarioNaoEncontrado(PizzariaException):
    """Exceção quando usuário não é encontrado"""
    def __init__(self, usuario_id: int = None, email: str = None):
        if usuario_id:
            message = f"Usuário com ID {usuario_id} não encontrado"
        elif email:
            message = f"Usuário com email {email} não encontrado"
        else:
            message = "Usuário não encontrado"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class PedidoNaoEncontrado(PizzariaException):
    """Exceção quando pedido não é encontrado"""
    def __init__(self, pedido_id: int):
        message = f"Pedido com ID {pedido_id} não encontrado"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ProdutoNaoEncontrado(PizzariaException):
    """Exceção quando produto não é encontrado"""
    def __init__(self, produto_id: int):
        message = f"Produto com ID {produto_id} não encontrado"
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class EmailJaCadastrado(PizzariaException):
    """Exceção quando email já está cadastrado"""
    def __init__(self, email: str):
        message = f"Email {email} já está cadastrado"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ProdutoJaExiste(PizzariaException):
    """Exceção quando produto já existe"""
    def __init__(self, nome: str, tamanho: str):
        message = f"Produto '{nome}' no tamanho '{tamanho}' já existe"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class CredenciaisInvalidas(PizzariaException):
    """Exceção para credenciais inválidas"""
    def __init__(self):
        message = "Email ou senha incorretos"
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class UsuarioInativo(PizzariaException):
    """Exceção quando usuário está inativo"""
    def __init__(self):
        message = "Usuário inativo. Entre em contato com o administrador."
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class SemPermissao(PizzariaException):
    """Exceção quando usuário não tem permissão"""
    def __init__(self, acao: str = None):
        if acao:
            message = f"Você não tem permissão para {acao}"
        else:
            message = "Acesso negado. Você não tem permissão para esta ação."
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class StatusInvalido(PizzariaException):
    """Exceção para status inválido"""
    def __init__(self, status_fornecido: str, status_validos: list):
        message = f"Status '{status_fornecido}' inválido. Use um dos seguintes: {', '.join(status_validos)}"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class ProdutoIndisponivel(PizzariaException):
    """Exceção quando produto está indisponível"""
    def __init__(self, produto_nome: str):
        message = f"Produto '{produto_nome}' não está disponível no momento"
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
