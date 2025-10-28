"""
Define as rotas (endpoints) da API para o recurso 'Categoria'.

Este módulo utiliza o APIRouter do FastAPI para agrupar as operações
CRUD (Create, Read) relacionadas a categorias.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.categoria import Categoria, CategoriaCreate
from app.services.categoria import CategoriaService

router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorias"]
)


@router.get(
    "/",
    response_model=List[Categoria],
    summary="Listar todas as categorias"
)
def read_categorias(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        service: CategoriaService = Depends(CategoriaService)
):
    """
    Obtém uma lista paginada de todas as categorias.
    """
    return service.get_categorias(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=Categoria,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova categoria (Admin)"
)
def create_categoria(
        categoria_in: CategoriaCreate,
        db: Session = Depends(get_db),
        service: CategoriaService = Depends(CategoriaService)
):
    """
    Cria uma nova categoria no banco de dados.
    """
    return service.create_categoria(db, categoria_in=categoria_in)
