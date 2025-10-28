"""
Repositório para o modelo PedidoItemModificador.

Esta classe é um repositório CRUD puro, herdando toda a sua
funcionalidade (create, get, get_multi, update, remove)
da classe BaseRepository.
"""

from app.models.pedido_item_modificador import PedidoItemModificador
from app.repositories.base import BaseRepository
from app.schemas.pedido_item_modificador import (
    PedidoItemModificadorCreate,
    PedidoItemModificadorUpdate
)


class PedidoItemModificadorRepository(
    BaseRepository[
        PedidoItemModificador,
        PedidoItemModificadorCreate,
        PedidoItemModificadorUpdate
    ]
):
    """
    Repositório para PedidoItemModificador, herdando de BaseRepository.

    Não contém métodos personalizados, apenas o CRUD genérico.
    """

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM PedidoItemModificador.
        """
        super().__init__(PedidoItemModificador)

    # -----------------------------------------------------------------
    # Todos os métodos (create, get, get_multi, update, remove)
    # são herdados da BaseRepository.
    #
    # O método 'create' original foi REMOVIDO por ser duplicado.
    # -----------------------------------------------------------------
