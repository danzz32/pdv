"""
Define a camada de serviço (lógica de negócios) para o recurso 'Categoria'.

Esta classe encapsula a lógica de negócios e coordena a interação com
o repositório de Categoria, tratando de validações antes de
acessar o banco de dados.
"""

# 1. Importações de terceiros (third-party)
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# 2. Importações locais da aplicação
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate, Categoria


class CategoriaService:
    """Camada de serviço para operações relacionadas a Categoria."""

    def __init__(self, repo: CategoriaRepository = Depends(CategoriaRepository)):
        """
        Inicializa o serviço com uma instância do repositório de Categoria,
        injetada como dependência pelo FastAPI.
        """
        self.repo = repo

    def create_categoria(
            self, db: Session, categoria_in: CategoriaCreate
    ) -> Categoria:  # Adicionada anotação de tipo de retorno
        """
        Cria uma nova categoria após validar se ela já existe.

        Args:
            db: A sessão da base de dados.
            categoria_in: Os dados da categoria a ser criada.

        Raises:
            HTTPException (400): Se uma categoria com o mesmo nome já existir.

        Returns:
            A entidade Categoria recém-criada.
        """
        db_categoria = self.repo.get_by_nome(db, nome=categoria_in.nome)
        if db_categoria:
            raise HTTPException(
                status_code=400,  # O status 400 (Bad Request) é mais comum aqui
                detail="Categoria já cadastrada."
            )
        return self.repo.create(db, categoria_in=categoria_in)

    def get_categorias(self, db: Session, skip: int = 0, limit: int = 100) -> list[Categoria]:
        """
        Busca uma lista paginada de categorias.

        Args:
            db: A sessão da base de dados.
            skip: O número de registros a pular.
            limit: O número máximo de registros a retornar.

        Returns:
            Uma lista de entidades Categoria.
        """
        return self.repo.get_multi(db, skip=skip, limit=limit)
