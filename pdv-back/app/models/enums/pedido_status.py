import enum


class PedidoStatus(enum.Enum):
    PENDENTE = "pendente"
    EM_PREPARACAO = "em preparação"
    CONCLUIDO = "concluído"
    CANCELADO = "cancelado"
