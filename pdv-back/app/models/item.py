import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, index=True)
    descricao = Column(String, nullable=True)
    preco_base = Column(Float)  # Preço do item sem nenhum adicional
    disponivel = Column(Boolean, default=True)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias.id"))

    # RELACIONAMENTOS
    categoria = relationship("Categoria", back_populates="itens")
    grupos_modificadores = relationship("GrupoModificador", back_populates="item")
    pedidos_onde_aparece = relationship("PedidoItem", back_populates="item")
