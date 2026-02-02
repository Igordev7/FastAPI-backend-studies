from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from dependencies import pegar_sessao
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone


auth_router = APIRouter(prefix="/auth",tags=["auth"])

def criar_token(id_usuario, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiracao_token = datetime.now(timezone.utc) + duracao_token 
    dic_info = {"id_user":id_usuario, "exp": expiracao_token}
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY, ALGORITHM)

    token = jwt_codificado
    return token

def verificar_token(token, session: Session = Depends(pegar_sessao)):
    
    user = session.query(Usuario).filter(Usuario.id == 1).first()
    return user

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    usuario = autenticar_usuario(usuario_schema.email, usuario_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400,detail="Usuario n encontrado ou credenciais invalidas")

    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token" : access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(token):
    usuario = verificar_token(token)
    access_token = criar_token(usuario.id)
    return {
            "access_token" : access_token,
            "token_type": "Bearer"
        }