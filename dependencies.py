from models import db
from sqlalchemy.orm import sessionmaker







def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        #retorna sem encerrar a sessão diferente do return
        yield session
    finally:
        session.close()