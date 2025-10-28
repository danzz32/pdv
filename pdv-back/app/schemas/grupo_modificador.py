"""
Define os schemas Pydantic (modelos de dados da API)
para o recurso 'GrupoModificador'.
"""

# 1. Importações de bibliotecas padrão
import uuid
# C0411: 'typing' (padrão) movido para antes de 'pydantic' (terceiros)
from typing import List, Optional

# 2. Importações de bibliotecas de terceiros
from pydantic import BaseModel, ConfigDict

# 3. Importações locais da aplicação
from .opcao_modificador import OpcaoModificador  # Importa o schema de leitura


# C0115: Adicionada docstring
class GrupoModificadorBase(BaseModel):
    """Campos base compartilhados para um grupo de modificadores."""
    nome: str
    min_selecao: int = 0
    max_selecao: int = 1


class GrupoModificadorCreate(GrupoModificadorBase):
    """Schema usado pelo repositório para criar."""
    item_id: uuid.UUID  # Precisa saber a qual item pertence


class GrupoModificadorUpdate(BaseModel):
    """Schema para atualizar (campos opcionais)."""
    nome: Optional[str] = None
    min_selecao: Optional[int] = None
    max_selecao: Optional[int] = None


class GrupoModificador(GrupoModificadorBase):
    """Schema para ler/retornar dados do grupo (aninhado)."""
    id: uuid.UUID
    opcoes: List[OpcaoModificador] = []  # Retorna as opções aninhadas

    model_config = ConfigDict(from_attributes=True)
