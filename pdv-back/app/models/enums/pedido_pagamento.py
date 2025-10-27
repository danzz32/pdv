import enum


class FormaPagamento(enum.Enum):
    PIX = "pix"
    CREDITO = "credito"
    DEBITO = "debito"
    DINHEIRO = "dinheiro"
