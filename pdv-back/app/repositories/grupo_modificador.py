"""
Repositório para o modelo GrupoModificador.

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como buscar todos os grupos de um item.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List, Optional, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.grupo_modificador import GrupoModificador
from app.repositories.base import BaseRepository
from app.schemas.grupo_modificador import (
    GrupoModificadorCreate,
    GrupoModificadorUpdate
)


class GrupoModificadorRepository(
    BaseRepository[GrupoModificador, GrupoModificadorCreate, GrupoModificadorUpdate]
):
    """
    Repositório para GrupoModificador, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM GrupoModificador.
        """
        super().__init__(GrupoModificador)

    def get_multi_by_item(
            self, db: Session, *, item_id: uuid.UUID
    ) -> list[type[GrupoModificador]]:
        """
        Busca todos os grupos modificadores associados a um item_id específico.

        (Este é um método personalizado que não está no BaseRepository)
        """
        return db.query(self.model).filter(item_id == self.model.item_id).all()
