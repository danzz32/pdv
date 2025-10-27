# app/repositories/opcao_modificador.py
from sqlalchemy.orm import Session
from app.models.opcao_modificador import OpcaoModificador
from app.schemas.opcao_modificador import *


class OpcaoModificadorRepository:

    def get(self, db: Session, id: uuid.UUID) -> OpcaoModificador | None:
        return db.query(OpcaoModificador).filter(OpcaoModificador.id == id).first()

    def get_multi_by_grupo(self, db: Session, grupo_id: uuid.UUID) -> list[type[OpcaoModificador]]:
        return db.query(OpcaoModificador) \
            .filter(grupo_id == OpcaoModificador.grupo_id).all()

    def create(self, db: Session, opcao_in: OpcaoModificadorCreate) -> OpcaoModificador:
        db_opcao = OpcaoModificador(
            **opcao_in.model_dump()
        )
        db.add(db_opcao)
        db.commit()
        db.refresh(db_opcao)
        return db_opcao

    def remove(self, db: Session, id: uuid.UUID) -> OpcaoModificador | None:
        db_obj = self.get(db, id=id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj


# opcao_modificador_repository = OpcaoModificadorRepository()
