# Pdv/pdv-back/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./delivery.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# C0103: Renomeado de 'SessionLocal' para 'SESSION_LOCAL'
SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SESSION_LOCAL()  # Atualizado aqui também
    try:
        yield db
    finally:
        db.close()
