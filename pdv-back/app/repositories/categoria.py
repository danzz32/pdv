# app/repositories/categoria.py (CORRIGIDO)
import uuid
from sqlalchemy.orm import Session

# --- CORREÇÃO DE IMPORTAÇÃO ---
# Importamos o modelo com um alias
from ..models.categoria import Categoria as CategoriaModel
# Importamos o módulo de schemas
from app.schemas.categoria import *


# --- FIM DA CORREÇÃO ---


class CategoriaRepository:

    def get(self, db: Session, id: uuid.UUID) -> CategoriaModel | None:
        # Usa o alias CategoriaModel
        return db.query(CategoriaModel).filter(id == CategoriaModel.id).first()

    def get_by_nome(self, db: Session, nome: str) -> CategoriaModel | None:
        # Usa o alias CategoriaModel
        return db.query(CategoriaModel).filter(nome == CategoriaModel.nome).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[CategoriaModel]:
        # Usa o alias CategoriaModel
        return db.query(CategoriaModel).offset(skip).limit(limit).all()

    def create(self, db: Session, categoria_in: CategoriaCreate) -> CategoriaModel:
        # Usa o alias CategoriaModel
        db_categoria = CategoriaModel(nome=categoria_in.nome)
        db.add(db_categoria)
        db.commit()
        db.refresh(db_categoria)
        return db_categoria

    def remove(self, db: Session, id: uuid.UUID) -> CategoriaModel | None:
        db_obj = self.get(db, id=id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj
