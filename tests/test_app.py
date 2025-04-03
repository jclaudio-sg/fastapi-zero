from http import HTTPStatus

from fastapi.testclient import TestClient

from src.fast_api_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # 1. Arrange - Organização
    response = client.get('/')  # 2. Act - Ação
    assert response.status_code == HTTPStatus.OK  # 3. Assert
    assert response.json() == {'message': 'Ola mundo!'}  # 3. Assert
