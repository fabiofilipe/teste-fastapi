"""Configuração do banco de dados"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

# Criando conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criando base para os modelos
Base = declarative_base()

# Criando SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
