"""
Define a camada de serviço (lógica de negócios) para 'Usuário'.

Responsável pela lógica de criação de usuários, validação de duplicados,
e gerenciamento de senhas (hashing e verificação).
"""

# 1. Importações da biblioteca padrão
from typing import Optional

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends  # Importação 'Depends' é crucial

# 3. Importações locais da aplicação
from app.schemas.user import User, UserCreate  # Importação explícita
from app.repositories.user import UserRepository  # Importação absoluta

# Configuração do Hashing de Senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Camada de serviço para lógica de negócios de Usuário."""

    # --- Refatoração de Clean Code (Injeção de Dependência) ---
    # O __init__ deve usar Depends() para que o FastAPI possa injetar
    # corretamente o repositório (que por sua vez recebe a sessão 'db').
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        """
        Inicializa o serviço injetando o repositório de usuário.
        """
        self.repository = repository

    def get_password_hash(self, password: str) -> str:
        """Gera o hash de uma senha em texto plano."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se a senha em texto plano bate com o hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Cria um novo usuário.

        - Valida se o e-mail já existe.
        - Faz o hash da senha.
        - Persiste no banco de dados.
        """
        db_user = self.repository.get_by_email(db, email=user_in.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado."
            )

        # Faz o hash da senha ANTES de enviar ao repositório
        hashed_password = self.get_password_hash(user_in.password)

        # Cria um novo schema de entrada para o repositório
        # (Boa prática para garantir que o 'user_in' original não seja modificado)
        repo_user_in = UserCreate(
            email=user_in.email,
            nome=user_in.nome,
            password=hashed_password  # Agora envia o hash
        )

        return self.repository.create(db, user_in=repo_user_in)

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Busca um usuário pelo seu e-mail."""
        return self.repository.get_by_email(db, email=email)
