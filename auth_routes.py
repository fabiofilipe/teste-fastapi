from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
#auth == autenticação


auth_router = APIRouter(prefix="/auth", tags=["auth"]) 

#token manual, ##ATENÇÃO melhorar isso aqui gerar um token de respeito 
def criar_token(id_usuario):
    token = f"sdjbsdijbsd{id_usuario}"
    return token

@auth_router.get("/")
async def home():
    #comentário -> docstring
    """
    Essa é a rota padrão de autenticação. Todas as rotas precisam de autenticação.
    Somente usuários autenticados podem acessar as rotas protegidas.
    """
    return {"mensagem": "Voce acessou a rota padrão de autenticação", "autenticado": False}
#400 deu errado, 200 para ok
@auth_router.post("/criar_conta")
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
        return {"mensagem": f"Usuário {usuario_Schema.email} cadastrado com sucesso!"}
        #return {"mensagem": "Usuário cadastrado com sucesso!"}

@auth_router.post("/login")    
async def login(login_schemas:LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==login_schemas.email).first()
    #usado o query para pesquisa no banco de dados, os demais . são como consultas SQL
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")
    else:
        access_token = criar_token(usuario.id)
        return {"access_token": access_token,
                "token_type": "Bearer"
                }