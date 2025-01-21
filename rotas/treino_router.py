from fastapi import APIRouter, Depends
from modelos.treino_model import TreinoBase
from sqlmodel import Session
from database import get_session
from controles import treino_control

router = APIRouter()

@router.get("/Treinos/{pagina}")
def get_treinos(pagina: int, session: Session = Depends(get_session)):
    return treino_control.select_treinos(pagina, 5, session)

@router.get("/Treinos/id/{treino_id}")
def get_treino_id(treino_id: int, session: Session = Depends(get_session)):
    return treino_control.select_treino_id(treino_id, session)

@router.get("/Treinos/dia/{dia_semana}/{pagina}")
def get_treinos_dia_semana(dia_semana: str, pagina: int, session: Session = Depends(get_session)):
    return treino_control.select_treinos_dia_semana(dia_semana, pagina, 5, session)

@router.post("/Treinos")
def post_treino(treino_base: TreinoBase, aluno_id: int, session: Session = Depends(get_session)):
    return treino_control.insert_treino(treino_base, aluno_id, session)

@router.delete("/Treinos/{treino_id}")
def delete_treino(treino_id: int, session: Session = Depends(get_session)):
    return treino_control.delete_treino(treino_id, session)

@router.put("/Treinos/{treino_id}")
def put_treino(treino_id: int, treino_base: TreinoBase, session: Session = Depends(get_session)):
    return treino_control.update_treino(treino_id, treino_base, session)