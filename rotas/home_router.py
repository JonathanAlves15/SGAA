from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def boas_vindas():
    return {"Mensagem": "Bem Vindo ao SGAA"}