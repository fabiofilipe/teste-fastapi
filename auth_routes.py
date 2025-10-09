from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
#auth == autenticação


auth_router = APIRouter(prefix="/auth", tags=["auth"]) 


#ss token e refresh token para que o usuario não precise está efetuando sempre login ou de tempo em tempo
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    #CRIANDO PERIODO DE EXPIRÇÃO DO TOKEN
    data_expiracao = datetime.now(timezone.utc) + duracao_token 
    #dicionario com informações do usuario, usando sub indicado pelo JWT para identificar o usuario
    # as "claims" do JWT devem seguir o padrão. "exp" para expiração e "sub" para o "subject" (usuário).
    # o valor de "sub" deve ser uma string.
    claims = {
        "sub": id_usuario,
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

#verificando se usuário 
def autenticar_usuario(email, senha, session: Session):
    #usado o query para pesquisa no banco de dados, os demais . são como consultas SQL
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get("/")
async def home():
    #comentário com """ -> docstring
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
        # Usando argumentos nomeados gostei como ficou visualmente #pensando em por em todos
        novo_usuario = Usuario(
            nome=usuario_Schema.nome,
            email=usuario_Schema.email,
            senha=senha_criptografada,
            ativo=usuario_Schema.ativo,
            admin=usuario_Schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário {usuario_Schema.email} cadastrado com sucesso!"}
        #return {"mensagem": "Usuário cadastrado com sucesso!"}

@auth_router.post("/login")    
async def login(login_schemas:LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schemas.email, login_schemas.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas ")
    else:
        access_token = criar_token(usuario.id)
        #usando refresh para duração de dias
        #access_token duração menor e mais exposto
        #refresh_token duração maior e não é transmitido com tanta frequência
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) 
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }