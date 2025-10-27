# app/routes/pedidos.py (ATUALIZADO)
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importar os schemas necessários explicitamente
from app.schemas.pedido import Pedido, PedidoCreateAPI, PedidoUpdate
from app.models.user import User
from ..database import get_db

from ..services.pedido import PedidoService
from ..auth import get_current_user, get_current_active_user

router = APIRouter(
    prefix="/api/pedidos",
    tags=["Pedidos"]
)


@router.post(
    "/",
    response_model=Pedido,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo pedido",
    description="Endpoint principal para submeter um novo pedido (carrinho)."
)
def create_pedido_endpoint(
        pedido_in: PedidoCreateAPI,
        db: Session = Depends(get_db),

        # --- CORREÇÃO ---
        # Injetamos a CLASSE PedidoService, não a instância
        service: PedidoService = Depends(PedidoService),
        # --- FIM DA CORREÇÃO ---

        current_user: Optional[User] = Depends(get_current_user)
):
    try:
        return service.create_pedido(db=db, pedido_in=pedido_in, current_user=current_user)
    except HTTPException as e:
        raise e
    except Exception as e:
        # É uma boa prática logar o 'e' aqui
        raise HTTPException(status_code=500, detail="Erro interno ao processar o pedido.")


@router.get(
    "/session/{session_id}",
    response_model=Pedido,
    summary="Buscar pedido por Sessão (Anônimo)",
    description="Permite que um cliente anônimo (guest) consulte o status do seu pedido."
)
def get_pedido_by_session(
        session_id: str,
        db: Session = Depends(get_db),

        # --- CORREÇÃO ---
        service: PedidoService = Depends(PedidoService)
        # --- FIM DA CORREÇÃO ---
):
    # Acessamos o repositório através da instância 'service' injetada
    db_pedido = service.pedido_repo.get_by_session_id(db, session_id=session_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return db_pedido


@router.get(
    "/me",
    response_model=List[Pedido],
    summary="Listar meus pedidos (Logado)",
    description="Retorna o histórico de pedidos do usuário autenticado."
)
def get_meus_pedidos(
        db: Session = Depends(get_db),

        # --- CORREÇÃO ---
        service: PedidoService = Depends(PedidoService),
        # --- FIM DA CORREÇÃO ---

        current_user: User = Depends(get_current_active_user)
):
    return service.pedido_repo.get_multi_by_usuario(db, usuario_id=current_user.id)


@router.patch(
    "/{pedido_id}/status",
    response_model=Pedido,
    summary="Atualizar status do pedido (Admin)",
    description="Usado pelo painel do admin para mudar o status (Ex: PENDENTE -> EM_PREPARACAO)."
)
def update_pedido_status(
        pedido_id: uuid.UUID,
        status_in: PedidoUpdate,
        db: Session = Depends(get_db),

        # --- CORREÇÃO ---
        service: PedidoService = Depends(PedidoService)
        # --- FIM DA CORREÇÃO ---
):
    db_pedido = service.pedido_repo.get(db, id=pedido_id)
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return service.pedido_repo.update_status(db, db_pedido=db_pedido, status=status_in.status)
