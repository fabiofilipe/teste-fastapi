from pydantic import BaseModel 
from typing import Optional


#usa o sqlalchemy.orm para converter o modelo do sqlalchemy em um modelo pydantic
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] 
    admin: Optional[bool] 

    class Config:
        from_attributes = True