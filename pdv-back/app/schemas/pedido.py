"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'Pedido'. Inclui schemas de entrada (input)
e schemas de saída (leitura).
"""

# 1. Importações de bibliotecas padrão
import uuid
from datetime import datetime
from typing import List, Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict

# 3. Importações locais da aplicação
from app.models.pedido import FormaPagamento, PedidoStatus
from .pedido_item import PedidoItem
from .user import User


# --- Schemas de ENTRADA (Input) para a API ---


class PedidoItemModificadorInput(BaseModel):
    """Schema de entrada para um modificador de item de pedido."""
    opcao_modificador_id: uuid.UUID


class PedidoItemInput(BaseModel):
    """Schema de entrada para um item de pedido (carrinho)."""
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
    """Campos base compartilhados para schemas de Pedido."""
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
    """Schema para atualizar o status de um pedido."""
    status: PedidoStatus


class Pedido(PedidoBase):
    """Schema para ler/retornar um pedido completo."""
    id: uuid.UUID
    data_criacao: datetime
    status: PedidoStatus
    forma_de_pagamento: FormaPagamento
    nome_cliente_anonimo: Optional[str] = None

    usuario: Optional[User] = None  # Dados do usuário (se houver)
    itens: List[PedidoItem] = []  # Lista de itens do pedido

    model_config = ConfigDict(from_attributes=True)
