from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()  # carrega as variáveis de ambiente do arquivo .env

#pega a variavel de ambiente SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

#rodar: uvicorn main:app --reload

app = FastAPI()  #  a variável precisa se chamar exatamente "app"

#deprecated -> evitar avisos de versões antigas de bibliotecas
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

