"""Testes para o módulo principal da Fast API."""

from http import HTTPStatus


def test_read_root(client) -> None:
    """Testa se a rota raiz retorna a mensagem Hello, World.

    Esse teste tem 3 partes (AAA - Arrange, Act, Assert):
    1. Arrange: configurar o teste
    2. Act: executar o teste (o SUT - System Under Test)
    3. Assert: verificar se o resultado é o esperado
    """
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}
