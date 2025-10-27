# app/schemas/pedido_item.py
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .pedido_item_modificador import PedidoItemModificador


# Schema simples para mostrar o item dentro do pedido
# (Evita circular import se importássemos o schema Item completo)
class ItemSimples(BaseModel):
    id: uuid.UUID
    nome: str
    model_config = ConfigDict(from_attributes=True)


class PedidoItemBase(BaseModel):
    quantidade: int
    observacoes: Optional[str] = None


class PedidoItemCreate(PedidoItemBase):
    """Schema usado pelo repositório para criar."""
    preco_unitario_base: float  # Snapshot do preço base
    pedido_id: uuid.UUID
    item_id: uuid.UUID


class PedidoItem(PedidoItemBase):
    """Schema para ler/retornar um item dentro de um pedido."""
    id: uuid.UUID
    preco_unitario_base: float
    item: ItemSimples  # O item base que foi comprado
    modificadores_escolhidos: List[PedidoItemModificador] = []

    model_config = ConfigDict(from_attributes=True)
