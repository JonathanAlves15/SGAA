from modelos.treino_model import Treino, TreinoBase
from modelos.aluno_model import Aluno
from sqlmodel import select, Session
from fastapi import HTTPException

def select_treinos(pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna todos os treinos por páginas 
    Args:
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): Valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        treinos: Retorna os treinos
    Raises:
        HTTPException: Caso nenhum treino for encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    treinos = session.exec(select(Treino).offset(offset).limit(tamanho_pagina)).all()
    if not treinos:
        raise HTTPException(status_code=404, detail="Nenhum treino encontrado")
    
    return treinos

def select_treino_id(treino_id: int, session: Session):
    """
    Retorna o treino do id em questão
    Args:
        treino_id (int): Id do treino
        session (Session): A sessão do banco de dados
    Returns:
        treinos: Retorna o treino
    Raises:
        HTTPException: Caso o treino não seja encontrado
    """ 
    treino = session.exec(select(Treino).where(Treino.id == treino_id)).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    return treino

def select_treinos_dia_semana(dia_semana: str, pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna o treino do dia da semana em questão
    Args:
        treino_id (int): Id do treino
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        treinos: Retorna o treino
    Raises:
        HTTPException: Caso o treino não seja encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    treinos = session.exec(select(Treino).where(Treino.dia_semana == dia_semana).offset(offset).limit(tamanho_pagina)).all()
    if not treinos:
        raise HTTPException(status_code=404, detail="Nenhum treino encontrado")
    
    return treinos

def insert_treino(treino_base: TreinoBase, aluno_id: int, session: Session):
    """
    Insere o treino e o associa a um aluno
    Args:
        treino_base (TreinoBase): Modelo base do treino
        aluno_id (int): Id do aluno
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno = session.get(Aluno, aluno_id)
    if aluno:
        treino_db = Treino(dia_semana=treino_base.dia_semana, aluno_id=aluno.id)
        session.add(treino_db)
        session.commit()
        session.refresh(treino_db)
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
def delete_treino(treino_id: int, session: Session):
    """
    Deleta o treino do id em questão
    Args:
        treino_id (int): Id do treino
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o treino não seja encontrado
    """ 
    treino = session.get(Treino, treino_id)
    if treino:
        session.delete(treino)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
def update_treino(treino_id: int, treino_base: TreinoBase, session: Session):
    """
    Atualiza o treino do id em questão
    Args:
        treino_id (int): Id do treino
        treino_base: (TreinoBase): Modelo base do treino
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o treino não seja encontrado
    """ 
    treino_db = session.get(Treino, treino_id)
    if treino_db:
        treino_db.dia_semana = treino_base.dia_semana
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Treino não encontrado")