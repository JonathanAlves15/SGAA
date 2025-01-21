from modelos.aluno_model import Aluno, AlunoBase
from modelos.treino_model import Treino
from sqlmodel import select, Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload, contains_eager

def insert_aluno(aluno_base: AlunoBase, session: Session):
    """
    Insere o aluno
    Args:
        aluno_base (AlunoBase): Modelo base do aluno
        session (Session): A sessão do banco de dados
    """
    aluno_db = Aluno(nome=aluno_base.nome, idade=aluno_base.idade)
    session.add(aluno_db)
    session.commit()
    session.refresh(aluno_db)

def select_alunos(pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna todos os alunos por páginas 
    Args:
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        alunos: Retorna os alunos
    Raises:
        HTTPException: Caso nenhum aluno for encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    alunos = session.exec(select(Aluno).offset(offset).limit(tamanho_pagina)).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado")
    
    return alunos

def select_quantidade_alunos(session: Session):
    """
    Retorna a quantidade de alunos
    Args:
        session (Session): A sessão do banco de dados
    Returns:
        alunos_numero: Retorna o número de alunos
    """ 
    alunos = session.exec(select(Aluno)).all()
    alunos_numero = len(alunos)
    
    return alunos_numero

def select_aluno_id(aluno_id: int, session: Session):
    """
    Retorna o aluno do id em questão
    Args:
        aluno_id (int): Id do aluno
        session (Session): A sessão do banco de dados
    Returns:
        aluno: Retorna um aluno
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno = session.exec(select(Aluno).where(Aluno.id == aluno_id)).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return aluno

def select_aluno_nome(aluno_nome: str, pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna o aluno do nome em questão
    Args:
        aluno_nome (str): Nome do aluno
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        alunos: Retorna os alunos
    Raises:
        HTTPException: Caso nenhum aluno for encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    alunos = session.exec(
        select(Aluno).where(Aluno.nome.like('%'+ aluno_nome + '%')).offset(offset).limit(tamanho_pagina)
    ).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado")
    
    return alunos

def select_aluno_treinos(aluno_id: int, session: Session):
    """
    Retorna os treinos do aluno do id em questão e os exercícios relacionados a cada treino
    Args:
        aluno_id (int): Id do aluno
        session (Session): A sessão do banco de dados
    Returns:
        treinos: Retorna os treinos e exercícios
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno_treinos = session.exec(
        select(Aluno).options(
            joinedload(Aluno.treinos)
        ).where(Aluno.id == aluno_id)
    ).unique()

    if aluno_treinos:
        treinos = []
        for aluno in aluno_treinos:
            treinos.append({
                "Treino": aluno.treinos
            })
            
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return treinos

def select_aluno_treino_dia_semana(aluno_id: int, dia_semana: str, session: Session):
    """
    Retorna os treinos de um dia da semana de um aluno do id em questão
    e os exercícios relacionados a cada treino
    Args:
        aluno_id (int): Id do aluno
        dia_semana (str): Dia da semana
        session (Session): A sessão do banco de dados
    Returns:
        treinos: Retorna os treinos e exercícios
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno_treinos = session.exec(
        select(Aluno).join(Aluno.treinos)
        .options(
            contains_eager(Aluno.treinos)
        ).filter(Aluno.id == aluno_id).filter(Treino.dia_semana == dia_semana)
    ).unique()

    if aluno_treinos:
        treinos = []
        for aluno in aluno_treinos:
            treinos.append({
                "Treino": aluno.treinos
            })
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return treinos

def select_aluno_data_inscricao(data_inscricao: datetime, pagina: int, tamanho_pagina: int, session: Session):
    """
    Retorna os alunos da data de inscrição em questão
    Args:
        data_inscricao (datetime): Id do aluno
        pagina (int): Valor para definir o offset
        tamanho_pagina (int): valor para definir o limit
        session (Session): A sessão do banco de dados
    Returns:
        alunos: Retorna os alunos
    Raises:
        HTTPException: Caso nenhum aluno for encontrado
    """ 
    offset = (pagina - 1) * tamanho_pagina
    alunos = session.exec(
        select(Aluno).where(Aluno.data_inscricao == data_inscricao)
        .offset(offset).limit(tamanho_pagina)
    ).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado")
    
    return alunos

def delete_aluno(aluno_id: int, session: Session):
    """
    Deleta o aluno do id em questão
    Args:
        aluno_id (int): Id do aluno
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno = session.get(Aluno, aluno_id)
    if aluno:
        session.delete(aluno)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

def update_aluno(aluno_id: int, aluno_base: AlunoBase, session: Session):
    """
    Atualiza o aluno do id em questão
    Args:
        aluno_id (int): Id do aluno
        aluno_base: (AlunoBase): Modelo base do aluno
        session (Session): A sessão do banco de dados
    Raises:
        HTTPException: Caso o aluno não seja encontrado
    """ 
    aluno_db = session.get(Aluno, aluno_id)
    if aluno_db:
        aluno_db.nome = aluno_base.nome
        aluno_db.idade = aluno_base.idade
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")