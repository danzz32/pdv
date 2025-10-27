import uuid
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from ..database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, unique=True, index=True)
    itens = relationship("Item", back_populates="categoria")
