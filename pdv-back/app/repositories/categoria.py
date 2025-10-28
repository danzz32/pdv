"""
Repositório para o modelo Categoria.

Esta classe herda o CRUD genérico de BaseRepository e implementa
métodos específicos para Categoria, como a busca por nome.
"""

# 1. Importações da biblioteca padrão
from typing import Optional

# 2. Importações de terceiros (third-party)
from sqlalchemy.orm import Session

# 3. Importações locais da aplicação
from app.models.categoria import Categoria
from app.repositories.base import BaseRepository
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


# A classe agora herda de BaseRepository
class CategoriaRepository(
    BaseRepository[Categoria, CategoriaCreate, CategoriaUpdate]
):

    def __init__(self):
        """
        Inicializa o repositório base com o modelo ORM Categoria.
        """
        # Passa o modelo Categoria para a classe pai
        super().__init__(Categoria)

    def get_by_nome(self, db: Session, *, nome: str) -> Optional[Categoria]:
        """
        Busca uma categoria específica pelo nome.

        (Este é um método personalizado que não está no BaseRepository)
        """
        # Usamos self.model (definido no __init__) em vez de CategoriaModel
        return db.query(self.model).filter(nome == self.model.nome).first()
