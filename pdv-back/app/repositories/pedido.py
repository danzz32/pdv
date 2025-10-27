# app/repositories/pedido.py (ATUALIZADO)
import uuid
from typing import Any

from sqlalchemy.orm import Session
from app.models.pedido import Pedido
from app.schemas.pedido import *


class PedidoRepository:

    # ... (get, get_by_session_id, get_multi_by_usuario, get_multi não mudam) ...
    def get(self, db: Session, id: uuid.UUID) -> Pedido | None:
        return db.query(Pedido).filter(Pedido.id == id).first()

    def get_by_session_id(self, db: Session, session_id: str) -> Pedido | None:
        return db.query(Pedido).filter(session_id == Pedido.session_id).first()

    def get_multi_by_usuario(self, db: Session, usuario_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[
        type[Pedido]]:
        return db.query(Pedido) \
            .filter(usuario_id == Pedido.usuario_id) \
            .order_by(Pedido.data_criacao.desc()) \
            .offset(skip).limit(limit).all()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> list[type[Pedido]]:
        return db.query(Pedido) \
            .order_by(Pedido.data_criacao.desc()) \
            .offset(skip).limit(limit).all()

    def create(self, db: Session, pedido_in: PedidoCreate) -> Pedido:
        db_pedido = Pedido(
            valor_total=pedido_in.valor_total,
            usuario_id=pedido_in.usuario_id,
            session_id=pedido_in.session_id,

            # --- NOVOS CAMPOS ---
            forma_de_pagamento=pedido_in.forma_de_pagamento,
            nome_cliente_anonimo=pedido_in.nome_cliente_anonimo
            # --- FIM NOVOS ---
        )
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido

    def update_status(self, db: Session, db_pedido: Pedido,
                      status: PedidoStatus) -> Pedido:
        db_pedido.status = status
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido


# pedido_repository = PedidoRepository()
