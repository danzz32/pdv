# app/repositories/pedido_item.py
import uuid
from typing import Any

from sqlalchemy.orm import Session
from app.models.pedido_item import PedidoItem
from app.schemas.pedido_item import *


class PedidoItemRepository:

    def create(self, db: Session,
               pedido_item_in: PedidoItemCreate) -> PedidoItem:
        db_pedido_item = PedidoItem(
            quantidade=pedido_item_in.quantidade,
            preco_unitario_base=pedido_item_in.preco_unitario_base,
            observacoes=pedido_item_in.observacoes,
            pedido_id=pedido_item_in.pedido_id,
            item_id=pedido_item_in.item_id
        )
        db.add(db_pedido_item)
        db.commit()
        db.refresh(db_pedido_item)
        return db_pedido_item

    def get_multi_by_pedido(self, db: Session, pedido_id: uuid.UUID) -> list[type[PedidoItem]]:
        return db.query(PedidoItem) \
            .filter(pedido_id == PedidoItem.pedido_id).all()


# pedido_item_repository = PedidoItemRepository()
