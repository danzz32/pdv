# app/repositories/item.py
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import *


class ItemRepository:

    def get(self, db: Session, id: uuid.UUID) -> Item | None:
        return db.query(Item).filter(Item.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[type[Item]]:
        return db.query(Item).offset(skip).limit(limit).all()

    def get_multi_by_categoria(self, db: Session, categoria_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[
        type[Item]]:
        return db.query(Item) \
            .filter(categoria_id == Item.categoria_id) \
            .offset(skip).limit(limit).all()

    def create(self, db: Session, item_in: ItemCreate) -> Item:
        db_item = Item(
            **item_in.model_dump()  # Assume que os nomes dos campos são iguais
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def update(self, db: Session, db_item: Item, item_in: ItemUpdate) -> Item:
        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def remove(self, db: Session, id: uuid.UUID) -> Item | None:
        db_obj = self.get(db, id=id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

# item_repository = ItemRepository()
