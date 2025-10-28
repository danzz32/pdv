"""Módulo placeholder para autenticação e verificação de usuário."""

from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException

from app.models.user import User


# --- PLACEHOLDER DE AUTENTICAÇÃO ---
# TODO: Substituir por uma dependência OAuth2 real que
# decodifica um token JWT e retorna o usuário do banco.

async def get_current_user() -> Optional[User]:
    """
    Dependência stub. Atualmente retorna None (usuário anônimo).
    Quando a autenticação JWT estiver implementada, 
    isto irá decodificar o token e buscar o usuário.
    """
    return None


async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    """
    Dependência que EXIGE um usuário logado.
    Irá falhar se get_current_user retornar None.
    """
    if user is None:
        # TODO: Quando o auth estiver pronto, mudar para 401 Unauthorized
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Não autenticado (Implementação de Auth pendente)"
        )
    return user
