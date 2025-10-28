"""
Define a camada de serviço (lógica de negócios) para o recurso 'Item'.

Coordena as operações com os repositórios de Item e Categoria,
aplicando validações como a existência de um item ou de uma categoria associada.
"""

# 1. Importações da biblioteca padrão
import uuid
from typing import List

# 2. Importações de terceiros (third-party)
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.item import Item as ItemModel  # Importando o modelo ORM
from app.repositories.categoria import CategoriaRepository
from app.repositories.item import ItemRepository
from app.schemas.item import Item, ItemCreate, ItemUpdate


class ItemService:
    """Camada de serviço para operações relacionadas a Item."""

    def __init__(
            self,
            item_repo: ItemRepository = Depends(ItemRepository),
            cat_repo: CategoriaRepository = Depends(CategoriaRepository)
    ):
        """
        Injeta os repositórios de Item e Categoria via dependência.
        """
        self.item_repo = item_repo
        self.cat_repo = cat_repo

    def _validate_categoria_exists(self, db: Session, categoria_id: uuid.UUID):
        """
        Rotina de validação centralizada para verificar se uma Categoria existe.

        Lança HTTPException 404 se a categoria não for encontrada.
        """
        db_categoria = self.cat_repo.get(db, id=categoria_id)
        if not db_categoria:
            raise HTTPException(
                status_code=404, detail="Categoria não encontrada."
            )

    def create_item(self, db: Session, item_in: ItemCreate) -> ItemModel:
        """
        Cria um novo item após validar a existência da categoria.
        """
        # Valida se a categoria associada existe
        self._validate_categoria_exists(db, item_in.categoria_id)

        return self.item_repo.create(db, item_in=item_in)

    def get_item(self, db: Session, item_id: uuid.UUID) -> ItemModel:
        """
        Busca um item específico pelo ID.

        Lança HTTPException 404 se o item não for encontrado.
        """
        db_item = self.item_repo.get(db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item não encontrado.")
        return db_item

    def get_items(
            self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ItemModel]:
        """
        Busca uma lista paginada de itens.
        """
        return self.item_repo.get_multi(db, skip=skip, limit=limit)

    def update_item(
            self, db: Session, item_id: uuid.UUID, item_in: ItemUpdate
    ) -> ItemModel:
        """
        Atualiza um item existente.

        Valida se o item existe e, se uma nova categoria for fornecida,
        valida também a nova categoria.
        """
        # Reusa a lógica de self.get_item() para validar se o item existe
        db_item = self.get_item(db, item_id)

        # Se o update incluir uma mudança de categoria, valida a nova categoria
        if item_in.categoria_id is not None:
            self._validate_categoria_exists(db, item_in.categoria_id)

        return self.item_repo.update(db, db_item=db_item, item_in=item_in)
