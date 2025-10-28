"""
Repositório para o modelo User (Usuário).

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como a busca por e-mail.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import Optional, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 3. Importações locais da aplicação
from app.models.user import User
from app.repositories.base import BaseRepository  # Importação da Base
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repositório para User, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM User.
        """
        super().__init__(User)

    # --- Métodos Sobrescritos (Overridden) para tratamento do Hashed Password ---

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Cria um novo usuário, mapeando 'password' do schema para
        'hashed_password' no modelo ORM.
        """
        # Converte o schema Pydantic para um dict, assumindo que
        # o 'password' aqui JÁ É O HASH.
        obj_in_data = obj_in.model_dump()

        # Mapeamento do campo: Remove 'password' e adiciona 'hashed_password'
        hashed_password = obj_in_data.pop("password")
        obj_in_data["hashed_password"] = hashed_password

        db_obj = self.model(**obj_in_data)  # Cria o modelo com os dados corrigidos

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Atualiza o usuário, tratando 'password' como 'hashed_password'.
        """
        # A lógica da BaseRepository funciona para a maioria dos campos,
        # mas precisamos intervir para o campo 'password'.

        update_data = obj_in.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"] is not None:
            # Assume que o serviço já fez o hash!
            update_data["hashed_password"] = update_data.pop("password")

        # Chama a lógica genérica de atualização da BaseRepository,
        # que agora fará a atualização usando 'hashed_password'.
        return super().update(db, db_obj=db_obj, obj_in=BaseModel(**update_data))

    # --- Métodos Específicos deste Repositório (Mantidos) ---

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Busca um usuário específico pelo seu endereço de e-mail."""
        return db.query(self.model).filter(email == self.model.email).first()
