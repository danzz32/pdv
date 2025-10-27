# app/schemas/opcao_modificador.py
import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional


class OpcaoModificadorBase(BaseModel):
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
