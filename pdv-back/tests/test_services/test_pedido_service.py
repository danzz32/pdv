import pytest
import uuid
from fastapi import HTTPException
from unittest.mock import MagicMock, create_autospec
from app.services.pedido import PedidoService
from app.repositories.item import ItemRepository
from app.repositories.pedido import PedidoRepository
from app.schemas.pedido import PedidoCreateAPI, PedidoItemInput
from app.models.item import Item


# Usamos pytest-mock (fixture 'mocker')
def test_create_pedido_anonimo_sem_nome(mocker):
    """
    Testa se o serviço levanta um erro 400 se o usuário
    for anônimo E não fornecer um nome.
    """
    # 1. Setup (Mock dos Repos)
    # create_autospec é melhor pois ele imita a classe real
    mock_pedido_repo = create_autospec(PedidoRepository)
    mock_item_repo = create_autospec(ItemRepository)

    # Criar a instância do serviço com os mocks
    service = PedidoService(
        pedido_repo=mock_pedido_repo,
        item_repo=mock_item_repo,
        opcao_repo=MagicMock(),
        pedido_item_repo=MagicMock(),
        pedido_item_mod_repo=MagicMock()
    )

    # 2. Dados de Entrada
    # Pedido anônimo (current_user=None) e sem nome_cliente_anonimo
    pedido_in = PedidoCreateAPI(
        itens=[],
        forma_de_pagamento="pix",
        nome_cliente_anonimo=None
    )

    # 3. Execução e Assertiva
    with pytest.raises(HTTPException) as exc_info:
        service.create_pedido(db=MagicMock(), pedido_in=pedido_in, current_user=None)

    assert exc_info.value.status_code == 400
    assert "nome do cliente é obrigatório" in exc_info.value.detail


def test_validar_e_calcular_total_item_inexistente(mocker):
    """
    Testa se o _validar_e_calcular_total falha se um item_id não existir.
    """
    # 1. Setup
    mock_item_repo = create_autospec(ItemRepository)
    # 'get' retorna None (item não encontrado)
    mock_item_repo.get.return_value = None

    service = PedidoService(
        item_repo=mock_item_repo,
        pedido_repo=MagicMock(),
        opcao_repo=MagicMock(),
        pedido_item_repo=MagicMock(),
        pedido_item_mod_repo=MagicMock()
    )

    # 2. Dados de Entrada
    item_invalido = PedidoItemInput(item_id=uuid.uuid4(), quantidade=1)
    pedido_in = PedidoCreateAPI(
        itens=[item_invalido],
        forma_de_pagamento="pix"
    )

    # 3. Execução e Assertiva
    with pytest.raises(HTTPException) as exc_info:
        service._validar_e_calcular_total(db=MagicMock(), pedido_in=pedido_in)

    assert exc_info.value.status_code == 404
    assert "não encontrado" in exc_info.value.detail
