from sqlmodel import SQLModel, Field, Relationship
from modelos.treino_model import Treino
from pydantic import BaseModel

class ExercicioBase(BaseModel):
    nome: str
    descricao: str
    intervalo_descanso: int
    series: int
    repeticoes_serie: int

class Exercicio(SQLModel, table=True):
    __tablename__ = 'exercicios'
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    intervalo_descanso: int
    series: int
    repeticoes_serie: int
    treino_id: int = Field(default=None, foreign_key="treinos.id")
    treino: Treino = Relationship(back_populates="exercicios")