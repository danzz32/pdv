# app/services/user.py
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.schemas.user import *
from ..repositories.user import UserRepository

# Configuração do Hashing de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, repository=UserRepository):
        self.repository = repository

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        db_user = self.repository.get_by_email(db, email=user_in.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado."
            )

        # Faz o hash da senha ANTES de enviar ao repositório
        hashed_password = self.get_password_hash(user_in.password)

        # Cria um novo schema de entrada para o repositório
        repo_user_in = UserCreate(
            email=user_in.email,
            nome=user_in.nome,
            password=hashed_password  # Agora envia o hash
        )

        return self.repository.create(db, user_in=repo_user_in)

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return self.repository.get_by_email(db, email=email)


# Instância
user_service = UserService()
