# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.user import UserService
from app.auth import create_access_token  # Importa do nosso novo auth.py
from app.schemas.token import Token  # Importa o novo schema

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/token", response_model=Token)
def login_for_access_token(
        db: Session = Depends(get_db),
        service: UserService = Depends(UserService),
        # OAuth2PasswordRequestForm espera 'username' e 'password'
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint de login unificado.

    Recebe 'username' (que é o nosso email) e 'password' de um
    formulário (form-data).

    Retorna um JWT com 'role' e 'sub' (ID do usuário) se
    a autenticação for bem-sucedida.
    """
    user = service.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar o token JWT com o ID (sub) e o Role
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}
