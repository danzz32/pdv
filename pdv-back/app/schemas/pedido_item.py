"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'PedidoItem'.
"""

# 1. Importações de bibliotecas padrão
import uuid
from typing import List, Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict, Field

# 3. Importações locais da aplicação
from .pedido_item_modificador import PedidoItemModificador


# Schema simples para mostrar o item dentro do pedido
# (Evita circular import se importássemos o schema Item completo)
class ItemSimples(BaseModel):
    """Um schema simplificado para representar um Item dentro de um Pedido."""
    id: uuid.UUID
    nome: str
    model_config = ConfigDict(from_attributes=True)


class PedidoItemBase(BaseModel):
    """Campos base compartilhados para um item de pedido."""
    quantidade: int
    observacoes: Optional[str] = None


class PedidoItemCreate(PedidoItemBase):
    """Schema usado pelo repositório para criar."""
    preco_unitario_base: float  # Snapshot do preço base
    pedido_id: uuid.UUID
    item_id: uuid.UUID


class PedidoItemUpdate(PedidoItemBase):
    """
    Schema usado para atualizar um item de pedido existente.
    Todos os campos de PedidoItemBase são opcionais para permitir
    atualizações parciais (PATCH).
    """
    quantidade: Optional[int] = Field(None, gt=0)
    observacoes: Optional[str] = Field(None, max_length=500)
    # OBS: Campos como preco_unitario_base, pedido_id e item_id geralmente
    # NÃO são atualizáveis após a criação.


class PedidoItem(PedidoItemBase):
    """Schema para ler/retornar um item dentro de um pedido."""
    id: uuid.UUID
    preco_unitario_base: float
    item: ItemSimples  # O item base que foi comprado
    modificadores_escolhidos: List[PedidoItemModificador] = []

    model_config = ConfigDict(from_attributes=True)
