from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, User as UserSchema

from app.services.user import UserService
from ..database import get_db

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
def create_user_endpoint(
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
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
