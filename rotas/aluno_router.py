from fastapi import APIRouter, Depends
from modelos.aluno_model import AlunoBase
from controles import aluno_control
from sqlmodel import Session
from database import get_session
from datetime import datetime

router = APIRouter()

@router.post("/alunos")
def post_aluno(aluno_base: AlunoBase, session: Session = Depends(get_session)):
    return aluno_control.insert_aluno(aluno_base, session)

@router.get("/alunos/quantidade")
def get_alunos_quantidade(session: Session = Depends(get_session)):
    return aluno_control.select_quantidade_alunos(session)

@router.get("/alunos/{pagina}")
def get_alunos(pagina: int, session: Session = Depends(get_session)):
    return aluno_control.select_alunos(pagina, 5, session)

@router.get("/alunos/id/{aluno_id}")
def get_aluno_id(aluno_id: int, session: Session = Depends(get_session)):
    return aluno_control.select_aluno_id(aluno_id, session)

@router.get("/alunos/nome/{aluno_nome}/{pagina}")
def get_aluno_nome(aluno_nome: str, pagina: int, session: Session = Depends(get_session)):
    return aluno_control.select_aluno_nome(aluno_nome, pagina, 5, session)

@router.get("/alunos/id/{aluno_id}/treinos")
def get_aluno_id_treinos(aluno_id: int, session: Session = Depends(get_session)):
    return aluno_control.select_aluno_treinos(aluno_id, session)

@router.get("/alunos/id/{aluno_id}/treinos/{dia_semana}")
def get_aluno_id_treinos_dia_semana(aluno_id: int, dia_semana: str, session: Session = Depends(get_session)):
    return aluno_control.select_aluno_treino_dia_semana(aluno_id, dia_semana, session)

@router.get("/alunos/inscricao/{data_inscricao}/{pagina}")
def get_aluno_data_inscricao(data_inscricao: str, pagina: int, session: Session = Depends(get_session)):
    return aluno_control.select_aluno_data_inscricao(datetime.strptime(data_inscricao, "%Y-%m-%d").date(), pagina, 5, session)

@router.delete("/alunos/{aluno_id}")
def delete_aluno(aluno_id: int, session: Session = Depends(get_session)):
    return aluno_control.delete_aluno(aluno_id, session)

@router.put("/alunos/{aluno_id}")
def put_aluno(aluno_id: int, aluno_base: AlunoBase, session: Session = Depends(get_session)):
    return aluno_control.update_aluno(aluno_id, aluno_base, session)