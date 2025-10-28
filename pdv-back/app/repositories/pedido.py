"""
Repositório para o modelo Pedido.

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como buscas por sessão, por usuário e atualização de status.
Também sobrescreve 'get_multi' para adicionar ordenação padrão.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List, Optional, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.pedido import Pedido
from app.repositories.base import BaseRepository
from app.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoStatus


class PedidoRepository(BaseRepository[Pedido, PedidoCreate, PedidoUpdate]):
    """
    Repositório para Pedido, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM Pedido.
        """
        super().__init__(Pedido)

    # --- Métodos Sobrescritos (Overridden) ---

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[type[Pedido]]:
        """
        Busca uma lista paginada de pedidos, ordenada por data de criação
        (mais recentes primeiro).

        (Sobrescreve o get_multi base para adicionar ordenação).
        """
        return (
            db.query(self.model)
            .order_by(self.model.data_criacao.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # --- Métodos Específicos deste Repositório ---

    def get_by_session_id(
            self, db: Session, *, session_id: str
    ) -> Optional[Pedido]:
        """Busca um pedido pelo session_id (para clientes não logados)."""
        return (
            db.query(self.model)
            .filter(session_id == self.model.session_id)
            .first()
        )

    def get_multi_by_usuario(
            self,
            db: Session,
            *,
            usuario_id: uuid.UUID,
            skip: int = 0,
            limit: int = 100
    ) -> List[Pedido]:
        """Busca um histórico paginado de pedidos de um usuário específico."""
        return (
            db.query(self.model)
            .filter(self.model.usuario_id == usuario_id)
            .order_by(self.model.data_criacao.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
            self, db: Session, *, db_pedido: Pedido, status: PedidoStatus
    ) -> Pedido:
        """Atualiza o status de um pedido existente."""
        db_pedido.status = status
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        return db_pedido
