# app/models/pedido_item_modificador.py
import uuid
from sqlalchemy import Column, Float, ForeignKey, UUID
from sqlalchemy.orm import relationship
from ..database import Base


class PedidoItemModificador(Base):
    __tablename__ = "pedidos_itens_modificadores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Preço do modificador no momento da compra (snapshot)
    preco_cobrado = Column(Float, nullable=False)

    # Relacionamento: Este modificador pertence a um PedidoItem
    pedido_item_id = Column(UUID(as_uuid=True), ForeignKey("pedidos_itens.id"))
    pedido_item = relationship("PedidoItem", back_populates="modificadores_escolhidos")

    # Relacionamento: Este é o modificador que foi escolhido
    opcao_modificador_id = Column(UUID(as_uuid=True), ForeignKey("opcoes_modificadores.id"))
    opcao = relationship("OpcaoModificador")  # Rel simples, não precisa back_populates aqui