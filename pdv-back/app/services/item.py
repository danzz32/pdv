# app/services/item.py
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from app.schemas.item import *
from ..repositories.item import ItemRepository
from ..repositories.categoria import CategoriaRepository  # Para validar a categoria


class ItemService:
    def __init__(self,
                 item_repo: ItemRepository = Depends(ItemRepository),
                 cat_repo: CategoriaRepository = Depends(CategoriaRepository)):
        self.item_repo = item_repo
        self.cat_repo = cat_repo

    def create_item(self, db: Session, item_in: ItemCreate):
        db_categoria = self.cat_repo.get(db, id=item_in.categoria_id)
        if not db_categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada.")

        return self.item_repo.create(db, item_in=item_in)

    def get_item(self, db: Session, item_id: uuid.UUID):
        db_item = self.item_repo.get(db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item não encontrado.")
        return db_item

    def get_items(self, db: Session, skip: int = 0, limit: int = 100):
        return self.item_repo.get_multi(db, skip=skip, limit=limit)

    def update_item(self, db: Session, item_id: uuid.UUID, item_in: ItemUpdate):
        db_item = self.get_item(db, item_id)  # Reusa a validação

        if item_in.categoria_id:
            db_categoria = self.cat_repo.get(db, id=item_in.categoria_id)
            if not db_categoria:
                raise HTTPException(status_code=404, detail="Categoria não encontrada.")

        return self.item_repo.update(db, db_item=db_item, item_in=item_in)
