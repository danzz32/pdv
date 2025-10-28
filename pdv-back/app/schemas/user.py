"""
Define os schemas (modelos Pydantic) para a entidade Usuário (User).

Estes schemas são usados para validação de dados, serialização e
desserialização de dados de entrada e saída da API.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import Optional

# 2. Importações de terceiros (third-party)
from pydantic import BaseModel, ConfigDict, EmailStr

# 3. Importações locais da aplicação
from app.models.user import UserRole  # Importa o Enum do modelo


class UserBase(BaseModel):
    """Schema base contendo os campos comuns de um usuário."""
    email: EmailStr
    nome: str


class UserCreate(UserBase):
    """Schema usado para criar um novo usuário."""
    password: str
    # Nota: O serviço é responsável por fazer o hash da senha
    # antes de enviá-la ao repositório.


class UserUpdate(BaseModel):
    """Schema para atualizar um usuário (todos os campos são opcionais)."""
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    password: Optional[str] = None  # Para reset de senha


class User(UserBase):
    """Schema para ler/retornar dados do usuário (resposta da API)."""
    id: uuid.UUID
    role: UserRole

    # Permite que o Pydantic mapeie os atributos do modelo ORM
    # diretamente para os campos deste schema.
    model_config = ConfigDict(from_attributes=True)
