import pytest
from fastapi.testclient import TestClient


def test_create_e_get_categorias_api(client: TestClient):
    """
    Testa o fluxo completo da API de Categorias.
    Este teste usa o fixture 'client' do conftest.py.
    """

    # 1. Criar uma nova categoria (POST)
    payload = {"nome": "Sobremesas"}
    response_post = client.post("/api/categorias/", json=payload)

    # 2. Assertivas do POST
    assert response_post.status_code == 201  # 201 Created
    data = response_post.json()
    assert data["nome"] == "Sobremesas"
    assert "id" in data
    categoria_id = data["id"]

    # 3. Buscar todas as categorias (GET)
    response_get = client.get("/api/categorias/")

    # 4. Assertivas do GET
    assert response_get.status_code == 200
    data_lista = response_get.json()

    assert isinstance(data_lista, list)
    assert len(data_lista) > 0

    # Verifica se o item criado está na lista
    nomes_na_lista = [item["nome"] for item in data_lista]
    ids_na_lista = [item["id"] for item in data_lista]

    assert "Sobremesas" in nomes_na_lista
    assert categoria_id in ids_na_lista
