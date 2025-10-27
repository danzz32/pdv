# app/schemas/pedido_item_modificador.py
import uuid
from pydantic import BaseModel, ConfigDict
from .opcao_modificador import OpcaoModificador


class PedidoItemModificadorBase(BaseModel):
    preco_cobrado: float  # Snapshot do preço no momento da compra


class PedidoItemModificadorCreate(PedidoItemModificadorBase):
    """Schema usado pelo repositório para criar."""
    pedido_item_id: uuid.UUID
    opcao_modificador_id: uuid.UUID


class PedidoItemModificador(PedidoItemModificadorBase):
    """Schema para ler/retornar o modificador escolhido."""
    id: uuid.UUID
    opcao: OpcaoModificador  # Detalhes da opção que foi escolhida

    model_config = ConfigDict(from_attributes=True)
