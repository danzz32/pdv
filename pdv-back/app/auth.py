# app/auth.py
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Importações locais da aplicação
from app.database import get_db
from app.repositories.user import UserRepository
from app.models.user import User, UserRole  # Importa o modelo User e o Enum

# --- Configuração do JWT ---
# (Em produção, mova para .env e use os.environ.get())
SECRET_KEY = "sua-chave-secreta-super-segura-aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia

# --- Esquema OAuth2 ---
# Esta é a URL que o cliente usará para obter o token (nossa rota de login)
# auto_error=False é CRUCIAL: permite que a dependência retorne None
# se o token não for fornecido (para login opcional).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)


# --- Funções de Utilitário JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um novo Access Token (JWT).
    'data' deve conter 'sub' (o ID do usuário) e 'role'.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- Exceções Padrão ---

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possível validar as credenciais",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Permissão insuficiente",
    headers={"WWW-Authenticate": "Bearer"},
)


# --- Dependências de Segurança ---

def get_optional_user(
        token: Optional[str] = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
        user_repo: UserRepository = Depends(UserRepository)
) -> Optional[User]:
    """
    Dependência 3 (Adaptada): Tenta buscar o usuário.
    Se não houver token ou se o token for inválido, retorna None.
    Não levanta erro.
    """
    if token is None:
        return None  # Nenhum token fornecido

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None  # Token inválido

    except JWTError:
        return None  # Token inválido (expirado, assinatura errada, etc.)

    user = user_repo.get(db, id=uuid.UUID(user_id))
    if user is None:
        return None  # Usuário não existe mais no DB

    return user


def get_current_user(
        user: Optional[User] = Depends(get_optional_user)
) -> User:
    """
    Dependência base que EXIGE um usuário logado (auto_error=True).
    Levanta 401 se 'get_optional_user' retornar None.
    """
    if user is None:
        raise credentials_exception  # Levanta 401
    return user


def get_current_admin(
        user: User = Depends(get_current_user)
) -> User:
    """
    Dependência 1 (Adaptada): Exige que o usuário seja um ADMIN.
    """
    if user.role != UserRole.ADMIN:
        raise forbidden_exception  # Levanta 403
    return user


def get_current_customer(
        user: User = Depends(get_current_user)
) -> User:
    """
    Dependência 2 (Adaptada): Exige que o usuário seja um CLIENTE.
    """
    if user.role != UserRole.CLIENTE:
        raise forbidden_exception  # Levanta 403
    return user
