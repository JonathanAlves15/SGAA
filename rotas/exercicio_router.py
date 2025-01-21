from fastapi import APIRouter, Depends
from modelos.exercicio_model import ExercicioBase
from sqlmodel import Session
from database import get_session
from controles import exercicio_control

router = APIRouter()

@router.get("/Exercicios/{pagina}")
def get_exercicios(pagina: int, session: Session = Depends(get_session)):
    return exercicio_control.select_exercicios(pagina, 5, session)

@router.get("/Exercicios/id/{exercicio_id}")
def get_exercicio_id(exercicio_id: int, session: Session = Depends(get_session)):
    return exercicio_control.select_exercicio_id(exercicio_id, session)

@router.get("/Exercicios/nome/{exercicion_nome}/{pagina}")
def get_exercicio_nome(exercicion_nome: str, pagina: int, session: Session = Depends(get_session)):
    return exercicio_control.select_exercicio_nome(exercicion_nome, pagina, 5, session)

@router.post("/Exercicios")
def post_exercicio(exercicio_base: ExercicioBase, treino_id: int, session: Session = Depends(get_session)):
    return exercicio_control.insert_exercicio(exercicio_base, treino_id, session)

@router.delete("/Exercicios/{exercicio_id}")
def delete_exercicio(exercicio_id: int, session: Session = Depends(get_session)):
    return exercicio_control.delete_exercicio(exercicio_id, session)

@router.put("/Exercicios/{exercicio_id}")
def put_exercicio(exercicio_id: int, exercicio_base: ExercicioBase, session: Session = Depends(get_session)):
    return exercicio_control.update_exercicio(exercicio_id, exercicio_base, session)