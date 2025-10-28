import uuid
from sqlalchemy import Column, String, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class OpcaoModificador(Base):
    __tablename__ = "opcoes_modificadores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)  # Ex: "Bacon", "Cheddar", "Ketchup"
    preco_adicional = Column(Float, default=0.0)

    # Relacionamento: Esta opção pertence a um grupo
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos_modificadores.id"))
    grupo = relationship("GrupoModificador", back_populates="opcoes")
