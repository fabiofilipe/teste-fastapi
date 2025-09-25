from fastapi import FastAPI

#rodar: uvicorn main:app --reload

app = FastAPI()  #  a variável precisa se chamar exatamente "app"

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

