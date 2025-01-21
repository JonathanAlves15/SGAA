from fastapi import FastAPI
from rotas import aluno_router, treino_router, exercicio_router, home_router
from database import criar_tabelas

criar_tabelas()

app = FastAPI()

app.include_router(aluno_router.router)
app.include_router(home_router.router)
app.include_router(treino_router.router)
app.include_router(exercicio_router.router)