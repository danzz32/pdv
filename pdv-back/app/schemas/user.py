# app/schemas/user.py
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from app.models.user import UserRole  # Importa o Enum do modelo


class UserBase(BaseModel):
    email: EmailStr
    nome: str


class UserCreate(UserBase):
    """Schema usado pelo repositório para criar."""
    password: str  # O serviço passará o hash para o repositório


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário (campos opcionais)."""
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    password: Optional[str] = None  # Para reset de senha


class User(UserBase):
    """Schema para ler/retornar dados do usuário."""
    id: uuid.UUID
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
