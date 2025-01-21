from modelos.treino_model import Treino
from modelos.exercicio_model import Exercicio, ExercicioBase
from sqlmodel import select, Session
from fastapi import HTTPException

def select_exercicios(pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna todos os exercício por páginas 
    Args:
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): Valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        exercicios: Retorna os exercícios
    Raises:
        HTTPException: Caso nenhum exercício for encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    exercicios = session.exec(select(Exercicio).offset(offset).limit(tamanho_pagina)).all()
    if not exercicios:
        raise HTTPException(status_code=404, detail="Nenhum exercício encontrado")
    
    return exercicios

def select_exercicio_id(exercicio_id: int, session: Session):
    """
    Retorna o exercício do id em questão
    Args:
        exercicio_id (int): Id do exercício
        session (Session): A sessão do banco de dados
    Returns:
        exercicios: Retorna o exercício
    Raises:
        HTTPException: Caso o exercício não seja encontrado
    """ 
    exercicio = session.exec(select(Exercicio).where(Exercicio.id == exercicio_id)).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    return exercicio

def select_exercicio_nome(exercicio_nome: str, pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna o exercício do nome em questão
    Args:
        exercicio_id (int): Id do exercício
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        exercicios: Retorna o exercício
    Raises:
        HTTPException: Caso o exercício não seja encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    exercicios = session.exec(
        select(Exercicio).where(Exercicio.nome.like('%'+ exercicio_nome + '%')).offset(offset).limit(tamanho_pagina)
    ).all()
    if not exercicios:
        raise HTTPException(status_code=404, detail="Nenhum exercício encontrado")
    
    return exercicios

def insert_exercicio(exercicio_base: ExercicioBase, treino_id: int, session: Session):
    """
    Insere o exercicio e o associa a um treino
    Args:
        exercicio_base (ExercicioBase): Modelo base do exercicio
        treino_id (int): Id do treino
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o treino não seja encontrado
    """ 
    treino = session.get(Treino, treino_id)

    if treino:
        exercicio_db = Exercicio(
            nome = exercicio_base.nome,
            descricao = exercicio_base.descricao,
            intervalo_descanso = exercicio_base.intervalo_descanso,
            series = exercicio_base.series,
            repeticoes_serie = exercicio_base.repeticoes_serie,
            treino_id = treino.id
        )
        session.add(exercicio_db)
        session.commit()
        session.refresh(exercicio_db)
    else:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
def delete_exercicio(exercicio_id: int, session: Session):
    """
    Deleta o exercício do id em questão
    Args:
        exercicio_id (int): Id do exercicio
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o exercício não seja encontrado
    """ 
    exercicio = session.get(Exercicio, exercicio_id)
    if exercicio:
        session.delete(exercicio)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
def update_exercicio(exercicio_id: int, exercicio_base: ExercicioBase, session: Session):
    """
    Atualiza o exercício do id em questão
    Args:
        exercicio_id (int): Id do exercício
        exercicio_base: (ExercicioBase): Modelo base do exercício
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o exercício não seja encontrado
    """ 
    exercicio_db = session.get(Exercicio, exercicio_id)
    if exercicio_db:
        exercicio_db.nome = exercicio_base.nome
        exercicio_db.descricao = exercicio_base.descricao
        exercicio_db.intervalo_descanso = exercicio_base.intervalo_descanso
        exercicio_db.series = exercicio_base.series
        exercicio_db.repeticoes_serie = exercicio_base.repeticoes_serie
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")