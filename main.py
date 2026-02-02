from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES =int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
bcrypt_context = CryptContext(schemes=["bcrypt"])

from order_routes import order_router
from auth_routes import auth_router

app.include_router(order_router)
app.include_router(auth_router)






#restAPi:

#Get - pegar/Ler
#Post - criar/enviar
#put/patch - edicao
#Delete - deletar