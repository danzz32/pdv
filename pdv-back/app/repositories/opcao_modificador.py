"""
Repositório para o modelo OpcaoModificador.

Herda o CRUD genérico de BaseRepository e implementa métodos
específicos, como buscar todas as opções de um grupo.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List, Optional, Any

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.opcao_modificador import OpcaoModificador
from app.repositories.base import BaseRepository
from app.schemas.opcao_modificador import (
    OpcaoModificadorCreate,
    OpcaoModificadorUpdate
)


class OpcaoModificadorRepository(
    BaseRepository[OpcaoModificador, OpcaoModificadorCreate, OpcaoModificadorUpdate]
):
    """
    Repositório para OpcaoModificador, herdando de BaseRepository.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM OpcaoModificador.
        """
        super().__init__(OpcaoModificador)

    def get_multi_by_grupo(
            self, db: Session, *, grupo_id: uuid.UUID
    ) -> list[type[OpcaoModificador]]:
        """
        Busca todas as opções de modificadores associadas a um grupo_id específico.

        (Este é um método personalizado que não está no BaseRepository)
        """
        return (
            db.query(self.model)
            .filter(grupo_id == self.model.grupo_id)
            .all()
        )
