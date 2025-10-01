from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session
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
#400 deu errado, 200 para ok
@auth_router.post("/login")
#: para o fastapi entender que é um parâmetro de query
#Depends -> injeção de dependência puxando o session da função pegar_sessao de dependencies.py
async def login(usuario_Schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_Schema.email).first()
    if usuario:
        #já existe esse usuário
        raise HTTPException(status_code=400, detail="Usuário já existe")
    else:   
        senha_criptografada = bcrypt_context.hash(usuario_Schema.senha)
        novo_usuario = Usuario(usuario_Schema.nome, usuario_Schema.email, senha_criptografada, usuario_Schema.ativo, usuario_Schema.admin,usuario_Schema.admin )
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário {usuario_Schema.nome} cadastrado com sucesso!"}
        #return {"mensagem": "Usuário cadastrado com sucesso!"}