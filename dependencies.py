from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session #yield retorna sem finalizar a função
    finally:
        session.close()