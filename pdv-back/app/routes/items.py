# app/routes/items.py
"""
Define as rotas (endpoints) da API para o recurso 'Item'.

Este módulo utiliza o APIRouter do FastAPI para agrupar as operações
CRUD (Create, Read, Update) relacionadas a itens do cardápio.
"""

# 1. Importações de bibliotecas padrão (standard library)
import uuid
from typing import List

# 2. Importações de bibliotecas de terceiros (third-party)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação (local application)
from app.database import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item import ItemService
from app.auth import get_current_admin  # <-- IMPORTAR DEPENDÊNCIA DE ADMIN

router = APIRouter(
    prefix="/api/items",
    tags=["Itens do Cardápio"]
)


@router.get(
    "/",
    response_model=List[Item],
    summary="Listar todos os itens do cardápio"
)
def read_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Obtém uma lista paginada de todos os itens do cardápio. (Público)
    """
    return service.get_items(db, skip=skip, limit=limit)


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Obter detalhes de um item"
)
def read_item(
        item_id: uuid.UUID,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Obtém os detalhes de um item específico pelo seu ID. (Público)
    """
    return service.get_item(db, item_id=item_id)


@router.post(
    "/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo item (Admin)",
    description="Cria um novo item no cardápio. (Requer role 'ADMIN')",
    dependencies=[Depends(get_current_admin)]
)
def create_item(
        item_in: ItemCreate,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Cria um novo item no cardápio.
    """
    return service.create_item(db, item_in=item_in)


@router.put(
    "/{item_id}",
    response_model=Item,
    summary="Atualizar um item (Admin)",
    description="Atualiza os detalhes de um item existente. (Requer role 'ADMIN')",
    dependencies=[Depends(get_current_admin)]
)
def update_item(
        item_id: uuid.UUID,
        item_in: ItemUpdate,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Atualiza os detalhes de um item existente.
    """
    return service.update_item(db, item_id=item_id, item_in=item_in)
