"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'Item'.
"""

# 1. Importações de bibliotecas padrão
import uuid
from typing import List, Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict

# 3. Importações locais da aplicação
from .categoria import Categoria
from .grupo_modificador import GrupoModificador


# C0115: Adicionada docstring
class ItemBase(BaseModel):
    """Campos base compartilhados para um item do cardápio."""
    nome: str
    descricao: Optional[str] = None
    preco_base: float
    disponivel: bool = True


class ItemCreate(ItemBase):
    """Schema usado pelo repositório para criar."""
    categoria_id: uuid.UUID  # Precisa saber a qual categoria pertence


class ItemUpdate(BaseModel):
    """Schema para atualizar (campos opcionais)."""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco_base: Optional[float] = None
    disponivel: Optional[bool] = None
    categoria_id: Optional[uuid.UUID] = None


class Item(ItemBase):
    """Schema para ler/retornar (cardápio)."""
    id: uuid.UUID
    categoria: Categoria  # Objeto Categoria aninhado
    grupos_modificadores: List[GrupoModificador] = []  # Lista de grupos aninhada

    model_config = ConfigDict(from_attributes=True)
