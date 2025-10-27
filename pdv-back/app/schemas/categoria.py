# app/schemas/categoria.py
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoriaBase(BaseModel):
    nome: str


class CategoriaCreate(CategoriaBase):
    """Schema usado pelo repositório para criar."""
    pass  # Nenhum campo extra necessário


class CategoriaUpdate(BaseModel):
    """Schema para atualizar (campos opcionais)."""
    nome: Optional[str] = None


class Categoria(CategoriaBase):
    """Schema para ler/retornar dados da categoria."""
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
