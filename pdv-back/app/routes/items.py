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
# Corrigido E0402 (importação relativa) e E0602/W0401 (wildcard)
from app.database import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter(
    prefix="/api/items",
    tags=["Itens do Cardápio"]
)


@router.get(
    "/",
    response_model=List[Item],  # 'List' e 'Item' agora estão definidos
    summary="Listar todos os itens do cardápio"
)
def read_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Obtém uma lista paginada de todos os itens do cardápio.
    """
    return service.get_items(db, skip=skip, limit=limit)


@router.get(
    "/{item_id}",
    response_model=Item,  # 'Item' agora está definido
    summary="Obter detalhes de um item"
)
def read_item(
        item_id: uuid.UUID,  # 'uuid' agora está definido
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Obtém os detalhes de um item específico pelo seu ID.
    """
    return service.get_item(db, item_id=item_id)


@router.post(
    "/",
    response_model=Item,  # 'Item' agora está definido
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo item (Admin)"
)
def create_item(
        item_in: ItemCreate,  # 'ItemCreate' agora está definido
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Cria um novo item no cardápio.
    """
    return service.create_item(db, item_in=item_in)


@router.put(
    "/{item_id}",
    response_model=Item,  # 'Item' agora está definido
    summary="Atualizar um item (Admin)"
)
def update_item(
        item_id: uuid.UUID,  # 'uuid' agora está definido
        item_in: ItemUpdate,  # 'ItemUpdate' agora está definido
        db: Session = Depends(get_db),
        service: ItemService = Depends(ItemService)
):
    """
    Atualiza os detalhes de um item existente.
    """
    return service.update_item(db, item_id=item_id, item_in=item_in)
