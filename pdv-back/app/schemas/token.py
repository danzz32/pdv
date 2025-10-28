# app/schemas/token.py
from pydantic import BaseModel


class Token(BaseModel):
    """Schema para a resposta do token JWT."""
    access_token: str
    token_type: str
