from sqlmodel import create_engine, SQLModel
from sqlmodel import Session
from sqlalchemy import inspect
import os

def get_db_type():
    database = os.getenv("DB_TYPE", "sqlite")

    if database == "postgresql":
        return "postgresql://postgres:1234@localhost:5432/SGAA"
    elif database == "sqlite":
        return "sqlite:///./database.db"
    else:
        raise ValueError(f"Banco de dados {database} não suportado")

def conexao_database():
    engine = create_engine(get_db_type())
    return engine

def criar_tabelas():
    engine = conexao_database()
    SQLModel.metadata.create_all(engine)
        
def get_session():
    engine = conexao_database()
    with Session(engine) as session:
        yield session