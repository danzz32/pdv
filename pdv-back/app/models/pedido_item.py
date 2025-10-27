# app/models/pedido_item.py
import uuid
from sqlalchemy import Column, Integer, Float, ForeignKey, UUID, String
from sqlalchemy.orm import relationship
from ..database import Base


class PedidoItem(Base):
    __tablename__ = "pedidos_itens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantidade = Column(Integer, nullable=False)

    preco_unitario_base = Column(Float, nullable=False)
    observacoes = Column(String, nullable=True)

    pedido_id = Column(UUID(as_uuid=True), ForeignKey("pedidos.id"))
    pedido = relationship("Pedido", back_populates="itens")

    # Relacionamento: Este item de pedido refere-se a um Item do cardápio
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="pedidos_onde_aparece")

    modificadores_escolhidos = relationship("PedidoItemModificador", back_populates="pedido_item")
