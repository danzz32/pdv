import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum, CheckConstraint, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from .enums.pedido_status import PedidoStatus
from .enums.pedido_pagamento import FormaPagamento


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(PedidoStatus), default=PedidoStatus.PENDENTE)
    valor_total = Column(Float)
    forma_de_pagamento = Column(Enum(FormaPagamento), nullable=False)
    nome_cliente_anonimo = Column(String, nullable=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    usuario = relationship("User", back_populates="pedidos")

    # Para checkout anônimo (guest)
    session_id = Column(String, index=True, nullable=True)

    # Itens dentro deste pedido
    itens = relationship("PedidoItem", back_populates="pedido")

    __table_args__ = (
        CheckConstraint(
            'usuario_id IS NOT NULL OR session_id IS NOT NULL',
            name='chk_pedido_identificador'
        ),
        # Garante que, se for anônimo, o nome seja fornecido
        CheckConstraint(
            'usuario_id IS NOT NULL OR nome_cliente_anonimo IS NOT NULL',
            name='chk_pedido_nome_anonimo'
        )
    )
