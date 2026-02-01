from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from models import Pedido
from dependencies import pegar_sessao
from sqlalchemy.orm import Session
order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedidos")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}
