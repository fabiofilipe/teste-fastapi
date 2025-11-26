"""Configurações da aplicação"""
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Configurações do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./banco.db")
