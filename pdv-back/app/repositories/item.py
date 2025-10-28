"""
Repositório para o modelo Item.

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como a busca paginada por categoria.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.item import Item
from app.repositories.base import BaseRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository(BaseRepository[Item, ItemCreate, ItemUpdate]):
    """
    Repositório para Item, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM Item.
        """
        super().__init__(Item)

    def get_multi_by_categoria(
            self,
            db: Session,
            *,
            categoria_id: uuid.UUID,
            skip: int = 0,
            limit: int = 100
    ) -> list[type[Item]]:
        """
        Busca uma lista paginada de itens pertencentes a uma categoria específica.

        (Este é um método personalizado que não está no BaseRepository)
        """
        return (
            db.query(self.model)
            .filter(categoria_id == self.model.categoria_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
