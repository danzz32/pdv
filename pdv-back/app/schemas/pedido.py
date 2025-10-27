# app/schemas/pedido.py (ATUALIZADO)
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from ..models.pedido import PedidoStatus, FormaPagamento
from .user import User
from .pedido_item import PedidoItem


# --- Schemas de ENTRADA (Input) para a API ---
class PedidoItemModificadorInput(BaseModel):
    opcao_modificador_id: uuid.UUID


class PedidoItemInput(BaseModel):
    item_id: uuid.UUID
    quantidade: int
    observacoes: Optional[str] = None
    modificadores: List[PedidoItemModificadorInput] = []


class PedidoCreateAPI(BaseModel):
    """Schema principal de entrada da API para criar um pedido."""
    session_id: Optional[str] = None  # Para guest checkout
    itens: List[PedidoItemInput]  # A lista de itens do carrinho

    forma_de_pagamento: FormaPagamento
    nome_cliente_anonimo: Optional[str] = None


# --- Schemas de Repositório e Leitura ---

class PedidoBase(BaseModel):
    valor_total: float  # O serviço irá calcular isso


class PedidoCreate(PedidoBase):
    """Schema usado pelo repositório para criar o Pedido."""
    usuario_id: Optional[uuid.UUID] = None
    session_id: Optional[str] = None

    # --- NOVOS CAMPOS PARA O REPO ---
    forma_de_pagamento: FormaPagamento
    nome_cliente_anonimo: Optional[str] = None
    # --- FIM NOVOS ---


class PedidoUpdate(BaseModel):
    status: PedidoStatus


class Pedido(PedidoBase):
    """Schema para ler/retornar um pedido completo."""
    id: uuid.UUID
    data_criacao: datetime
    status: PedidoStatus

    # --- NOVOS CAMPOS DE SAÍDA ---
    forma_de_pagamento: FormaPagamento
    nome_cliente_anonimo: Optional[str] = None
    # --- FIM NOVOS ---

    usuario: Optional[User] = None  # Dados do usuário (se houver)
    itens: List[PedidoItem] = []  # Lista de itens do pedido

    model_config = ConfigDict(from_attributes=True)
