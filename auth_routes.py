from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from dependencies import pegar_sessao
from main import bcrypt_context
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth",tags=["auth"])

def criar_token(id_usuario):
    token = f"jsdsofadaojf{id_usuario}"
    return token

@auth_router.get("/")
async def autenticar():
    """
    Rota padrão de autenticação
    """
    return {"mensagem": "Você acessou a rota de auth", "autenticado" : False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    else:
        senha_cripto = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome,usuario_schema.email,senha_cripto, usuario_schema.admin, usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem":"Usuario cadastrado com sucesso"}
    
# login -> email e senha -> token JWT sadhuahsuafuanudsand   
@auth_router.post("/login")
async def login(usuario_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400,detail="Usuario n encontrado")

    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token" : access_token,
            "token_type": "Bearer"
        }
