# app/routes/items.py (VERIFICADO)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.item import *
from ..database import get_db
from ..services.item import ItemService

router = APIRouter(
    prefix="/api/items",
    tags=["Itens do Cardápio"]
)


@router.get(
    "/",
    response_model=List[Item],  # <-- VERIFICADO: É um schema Pydantic
    summary="Listar todos os itens do cardápio"
)
def read_items_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)  # <-- Correto
):
    return service.get_items(db, skip=skip, limit=limit)


@router.get(
    "/{item_id}",
    response_model=Item,  # <-- VERIFICADO: É um schema Pydantic
    summary="Obter detalhes de um item"
)
def read_item_endpoint(
        item_id: uuid.UUID,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)  # <-- Correto
):
    return service.get_item(db, item_id=item_id)


@router.post(
    "/",
    response_model=Item,  # <-- VERIFICADO: É um schema Pydantic
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo item (Admin)"
)
def create_item_endpoint(
        item_in: ItemCreate,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)  # <-- Correto
):
    return service.create_item(db, item_in=item_in)


@router.put(
    "/{item_id}",
    response_model=Item,  # <-- VERIFICADO: É um schema Pydantic
    summary="Atualizar um item (Admin)"
)
def update_item_endpoint(
        item_id: uuid.UUID,
        item_in: ItemUpdate,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)  # <-- Correto
):
    return service.update_item(db, item_id=item_id, item_in=item_in)
