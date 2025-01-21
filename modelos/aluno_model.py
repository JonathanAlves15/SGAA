from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import date

class AlunoBase(BaseModel):
    nome: str
    idade: int

class Aluno(SQLModel, table=True):
    __tablename__ = 'alunos'
    id: int = Field(default=None, primary_key=True)
    nome: str
    idade: int
    data_inscricao: date = Field(default_factory=date.today)
    treinos: list["Treino"] | None = Relationship(back_populates="aluno", cascade_delete=True)