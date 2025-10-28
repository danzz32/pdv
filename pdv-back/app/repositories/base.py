# app/repositories/base.py
import uuid
from typing import Any, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import Base  # Importe seu Base declarativo do SQLAlchemy

# Define tipos genéricos
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Classe base genérica para repositórios (CRUD).

    Contém a lógica comum para Criar, Ler, Atualizar e Deletar (CRUD).
    """

    def __init__(self, model: Type[ModelType]):
        """
        Inicializa o repositório com o modelo ORM específico.
        ex: super().__init__(Item)
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Busca um objeto pelo seu ID."""
        # .get() é otimizado para busca por chave primária
        return db.query(self.model).get(id)

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Busca uma lista paginada de objetos."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Cria um novo objeto no banco."""
        # Converte o schema Pydantic para um dict
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)  # Desempacota o dict no modelo ORM
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """Atualiza um objeto existente no banco."""
        obj_data = db_obj.model_dump()
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        Deleta um objeto do banco pelo ID.
        (Este é o código que o Pylint marcou como duplicado)
        """
        db_obj = db.query(self.model).get(id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
