# app/routes/categorias.py (VERIFICADO)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.categoria import *
from ..database import get_db
from ..services.categoria import CategoriaService

router = APIRouter(
    prefix="/api/categorias",
    tags=["Categorias"]
)


@router.get(
    "/",
    response_model=List[Categoria],
    summary="Listar todas as categorias"
)
def read_categorias_endpoint(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        service: CategoriaService = Depends(CategoriaService)
):
    return service.get_categorias(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=Categoria,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova categoria (Admin)"
)
def create_categoria_endpoint(
        categoria_in: CategoriaCreate,
        db: Session = Depends(get_db),
        service: CategoriaService = Depends(CategoriaService)  # <-- Correto
):
    return service.create_categoria(db, categoria_in=categoria_in)
