# app/schemas/grupo_modificador.py
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .opcao_modificador import OpcaoModificador  # Importa o schema de leitura


class GrupoModificadorBase(BaseModel):
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
