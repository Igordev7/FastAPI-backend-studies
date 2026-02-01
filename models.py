from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#alembic faz migração de bd pra evitar a perda caso adicione alguma coisa


# cria a conexão do bd
db = create_engine("sqlite:///banco.db")

# cria a base do bd
Base = declarative_base()

# criar as classes/tabelas do bd
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer,primary_key=True ,autoincrement=True)
    nome =Column("nome", String)
    email =Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin =Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base): 
    __tablename__ = "pedidos"

    #STATUS_PEDIDOS = (
    #    ("PENDENTE", "PENDENTE"),
    #    ("CANCELADO", "cANCELADO"),
    #    ("FINALIZADO","FINALIZADO"),
    #    ("EM ANDAMENTO", "EM ANDAMENTO")
    #)

    id = Column("id", Integer, primary_key = True, autoincrement=True)
    status=Column("status", String) #pendente, cancelado, em andamento, finalizado

    usuario= Column("usuario", ForeignKey("usuarios.id"))
    preco= Column("preco", Float)

    def __init__(self, usuario, status = "PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status 

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    qtd = Column("quantidade", Integer)
    sabor = Column("Sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, qtd, sabor, tamanho, preco_unitario, pedido):
        self.qtd = qtd
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido





# executa a criação dos metadados do seu bd (cria efetivamente o seu bd)



