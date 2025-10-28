import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from typing import Generator

# Importar a Base e o app principal
from app.database import Base, get_db
from app.main import app

# --- 1. Configuração do Banco de Dados de Teste ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Fixture para criar o banco e as tabelas uma vez por sessão."""
    Base.metadata.create_all(bind=engine)
    yield engine
    # Limpeza (apaga o banco de teste após os testes rodarem)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Fixture para uma sessão de DB limpa para cada teste."""
    connection = db_engine.connect()
    # Inicia uma transação
    transaction = connection.begin()
    # Cria a sessão
    session = TestingSessionLocal(bind=connection)

    yield session  # O teste é executado aqui

    # Limpeza após o teste
    session.close()
    # Desfaz a transação (garante que cada teste comece do zero)
    transaction.rollback()
    connection.close()


# --- 2. Configuração do Cliente de Teste da API ---

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Fixture para o TestClient da API."""

    def override_get_db() -> Generator[Session, None, None]:
        """Substitui a dependência 'get_db' para usar o DB de teste."""
        try:
            yield db_session
        finally:
            db_session.close()  # Fechado pelo fixture 'db_session'

    # Substitui a dependência de produção pela de teste
    app.dependency_overrides[get_db] = override_get_db

    # Cria o cliente de teste
    with TestClient(app) as test_client:
        yield test_client

    # Remove a substituição após o teste
    app.dependency_overrides.clear()
