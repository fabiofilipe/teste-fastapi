from fastapi import APIRouter

#auth == autenticação


auth_router = APIRouter(prefix="/auth", tags=["auth"]) 

@auth_router.get("/")
async def autenticar():
    #comentário -> docstring
    """
    Essa é a rota padrão de autenticação. Todas as rotas precisam de autenticação.
    Somente usuários autenticados podem acessar as rotas protegidas.
    """
    return {"mensagem": "Voce acessou a rota padrão de autenticação", "autenticado": False}