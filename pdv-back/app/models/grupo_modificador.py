import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship
from ..database import Base


class GrupoModificador(Base):
    __tablename__ = "grupos_modificadores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)  # Ex: "Adicionais", "Escolha seu molho"

    # Regras de seleção
    min_selecao = Column(Integer, default=0)  # Ex: 0 para "Adicionais"
    max_selecao = Column(Integer, default=1)  # Ex: 1 para "Tamanho"

    # Relacionamento: Este grupo pertence a um item
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="grupos_modificadores")

    # Relacionamento: Este grupo contém várias opções
    opcoes = relationship("OpcaoModificador", back_populates="grupo")
