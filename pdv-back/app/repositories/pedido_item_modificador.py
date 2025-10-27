# app/repositories/pedido_item_modificador.py
import uuid
from sqlalchemy.orm import Session
from app.models.pedido_item_modificador import PedidoItemModificador
from app.schemas.pedido_item_modificador import *


class PedidoItemModificadorRepository:

    def create(self, db: Session,
               mod_in: PedidoItemModificadorCreate) -> PedidoItemModificador:
        db_mod = PedidoItemModificador(
            preco_cobrado=mod_in.preco_cobrado,
            pedido_item_id=mod_in.pedido_item_id,
            opcao_modificador_id=mod_in.opcao_modificador_id
        )
        db.add(db_mod)
        db.commit()
        db.refresh(db_mod)
        return db_mod


# pedido_item_modificador_repository = PedidoItemModificadorRepository()
