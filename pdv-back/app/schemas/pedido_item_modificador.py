"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'PedidoItemModificador'.
"""

# 1. Importações de bibliotecas padrão
import uuid

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict

# 3. Importações locais da aplicação
from .opcao_modificador import OpcaoModificador


class PedidoItemModificadorBase(BaseModel):
    """Campos base para um modificador de item de pedido."""
    preco_cobrado: float  # Snapshot do preço no momento da compra


class PedidoItemModificadorCreate(PedidoItemModificadorBase):
    """Schema usado pelo repositório para criar."""
    pedido_item_id: uuid.UUID
    opcao_modificador_id: uuid.UUID


class PedidoItemModificadorUpdate(BaseModel):
    """
    Schema para atualizar um PedidoItemModificador.
    (Atualmente não suporta atualizações - campos podem ser
    adicionados aqui se/quando necessário)
    """
    pass  # Nenhum campo é atualizável por enquanto


class PedidoItemModificador(PedidoItemModificadorBase):
    """Schema para ler/retornar o modificador escolhido."""
    id: uuid.UUID
    opcao: OpcaoModificador  # Detalhes da opção que foi escolhida

    model_config = ConfigDict(from_attributes=True)
