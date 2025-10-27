import pytest
from sqlalchemy.orm import Session
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate


def test_create_categoria(db_session: Session):
    """
    Testa a criação de uma categoria no banco de dados.
    Este teste usa o fixture 'db_session' do conftest.py.
    """
    # 1. Setup
    repo = CategoriaRepository()
    categoria_in = CategoriaCreate(nome="Bebidas")

    # 2. Execução
    db_categoria = repo.create(db=db_session, categoria_in=categoria_in)

    # 3. Assertivas
    assert db_categoria is not None
    assert db_categoria.id is not None
    assert db_categoria.nome == "Bebidas"


def test_get_by_nome(db_session: Session):
    """
    Testa a busca de uma categoria pelo nome.
    """
    # 1. Setup (Criar o dado primeiro)
    repo = CategoriaRepository()
    categoria_in = CategoriaCreate(nome="Sanduíches")
    db_categoria_criada = repo.create(db=db_session, categoria_in=categoria_in)

    # 2. Execução
    db_categoria_buscada = repo.get_by_nome(db=db_session, nome="Sanduíches")

    # 3. Assertivas
    assert db_categoria_buscada is not None
    assert db_categoria_buscada.id == db_categoria_criada.id
    assert db_categoria_buscada.nome == "Sanduíches"


def test_get_by_nome_nao_encontrado(db_session: Session):
    """Testa se retorna None se o nome não existir."""
    repo = CategoriaRepository()
    db_categoria = repo.get_by_nome(db=db_session, nome="Inexistente")
    assert db_categoria is None
