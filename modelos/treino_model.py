from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from modelos.aluno_model import Aluno

class TreinoBase(BaseModel):
    dia_semana: str

class Treino(SQLModel, table=True):
    __tablename__ = 'treinos'
    id: int | None = Field(default=None, primary_key=True)
    dia_semana: str
    aluno_id: int = Field(default=None, foreign_key="alunos.id")
    aluno: Aluno = Relationship(back_populates="treinos")
    exercicios: list["Exercicio"] = Relationship(back_populates="treino")
