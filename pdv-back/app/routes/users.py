"""
Define as rotas (endpoints) da API para o recurso 'Usuário'.

Este módulo utiliza o APIRouter do FastAPI para agrupar as operações
de criação (registro) de usuários.
"""

# 1. Importações de bibliotecas padrão (standard library)
from http import HTTPStatus

# 2. Importações de bibliotecas de terceiros (third-party)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação (local application)
from app.database import get_db
from app.schemas.user import UserCreate, User as UserSchema
from app.services.user import UserService

router = APIRouter(
    prefix="/api/users",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UserSchema,
    status_code=HTTPStatus.CREATED,
    summary="Criar um novo usuário (Cliente)",
    description="Registra um novo cliente no sistema. A senha será hasheada."
)
def create_user(
        user_in: UserCreate,
        db: Session = Depends(get_db),
        service: UserService = Depends(UserService)
):
    """
    Cria um novo usuário no banco de dados.
    - **user_in**: Dados do usuário (nome, email, senha).
    - **Retorna**: O usuário criado (sem a senha).
    - **Erros**: 400 se o email já estiver em uso.
    """
    try:
        return service.create_user(db=db, user_in=user_in)
    except HTTPException:
        raise  # Deixa o erro 400 do serviço passar
    except Exception as e:
        # Converte erros inesperados (500)
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao criar usuário: {e}"
        ) from e
