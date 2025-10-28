"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'Categoria'.
"""

# 1. Importações de bibliotecas padrão
import uuid
from typing import Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict


# C0115: Adicionada docstring para a classe base
class CategoriaBase(BaseModel):
    """Campos base compartilhados por todos os schemas de Categoria."""
    nome: str


class CategoriaCreate(CategoriaBase):
    """Schema usado pelo repositório para criar."""
    # W0107: 'pass' removido, pois a docstring já serve como corpo da classe


class CategoriaUpdate(BaseModel):
    """Schema para atualizar (campos opcionais)."""
    nome: Optional[str] = None


class Categoria(CategoriaBase):
    """Schema para ler/retornar dados da categoria."""
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
