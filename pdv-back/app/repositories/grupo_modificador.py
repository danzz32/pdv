# app/repositories/grupo_modificador.py

from sqlalchemy.orm import Session
from app.models.grupo_modificador import GrupoModificador
from app.schemas.grupo_modificador import *


class GrupoModificadorRepository:

    def get(self, db: Session, id: uuid.UUID) -> GrupoModificador | None:
        return db.query(GrupoModificador).filter(
            GrupoModificador.id == id).first()

    def get_multi_by_item(self, db: Session, item_id: uuid.UUID) -> list[type[GrupoModificador]]:
        return db.query(GrupoModificador) \
            .filter(item_id == GrupoModificador.item_id).all()

    def create(self, db: Session,
               grupo_in: GrupoModificadorCreate) -> GrupoModificador:
        db_grupo = GrupoModificador(
            **grupo_in.model_dump()
        )
        db.add(db_grupo)
        db.commit()
        db.refresh(db_grupo)
        return db_grupo

    def remove(self, db: Session, id: uuid.UUID) -> GrupoModificador | None:
        db_obj = self.get(db, id=id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj


# grupo_modificador_repository = GrupoModificadorRepository()
