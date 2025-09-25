from fastapi import APIRouter

#auth == autenticação


auth_router = APIRouter(prefix="/auth", tags=["auth"]) 

@auth_router.get("/")
async def autenticar():
    return {"mensagem": "Voce acessou a rota padrão de autenticação", "autenticado": False}