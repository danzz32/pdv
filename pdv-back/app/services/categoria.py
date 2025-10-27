# app/services/categoria.py
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.models.categoria import Categoria
from app.schemas.categoria import *
from ..repositories.categoria import CategoriaRepository


class CategoriaService:
    def __init__(self, repo: CategoriaRepository = Depends(CategoriaRepository)):
        self.repo = repo

    def create_categoria(self, db: Session, categoria_in: CategoriaCreate):
        db_categoria = self.repo.get_by_nome(db, nome=categoria_in.nome)
        if db_categoria:
            raise HTTPException(status_code=400, detail="Categoria já cadastrada.")
        return self.repo.create(db, categoria_in=categoria_in)

    def get_categorias(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repo.get_multi(db, skip=skip, limit=limit)
