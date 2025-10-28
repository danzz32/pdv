"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'OpcaoModificador'.
"""

# 1. Importações de bibliotecas padrão
import uuid
from typing import Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict


# C0115: Adicionada docstring
class OpcaoModificadorBase(BaseModel):
    """Campos base compartilhados para uma opção de modificador."""
    nome: str
    preco_adicional: float = 0.0


class OpcaoModificadorCreate(OpcaoModificadorBase):
    """Schema usado pelo repositório para criar."""
    grupo_id: uuid.UUID  # Precisa saber a qual grupo pertence


class OpcaoModificadorUpdate(BaseModel):
    """Schema para atualizar (campos opcionais)."""
    nome: Optional[str] = None
    preco_adicional: Optional[float] = None


class OpcaoModificador(OpcaoModificadorBase):
    """Schema para ler/retornar dados da opção."""
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)