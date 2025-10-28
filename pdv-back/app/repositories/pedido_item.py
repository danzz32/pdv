"""
Repositório para o modelo PedidoItem (os itens de um pedido).

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como buscar todos os itens de um pedido.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.pedido_item import PedidoItem
from app.repositories.base import BaseRepository
from app.schemas.pedido_item import PedidoItemCreate, PedidoItemUpdate


class PedidoItemRepository(
    BaseRepository[PedidoItem, PedidoItemCreate, PedidoItemUpdate]
):
    """
    Repositório para PedidoItem, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM PedidoItem.
        """
        super().__init__(PedidoItem)

    def get_multi_by_pedido(
            self, db: Session, *, pedido_id: uuid.UUID
    ) -> list[type[PedidoItem]]:
        """
        Busca todos os itens associados a um pedido_id específico.

        (Este é um método personalizado que não está no BaseRepository)
        """
        return (
            db.query(self.model)
            .filter(pedido_id == self.model.pedido_id)
            .all()
        )
