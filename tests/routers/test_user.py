from http import HTTPStatus

from fast_api.schemas import UserPublic


def test_create_user(client) -> None:
    """Testa se a rota de criação de usuário retorna o usuário criado."""
    response = client.post(
        '/users/',
        json={
            'username': 'novo_usuario',
            'email': 'novo@teste.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'novo_usuario',
        'email': 'novo@teste.com',
    }


def test_create_user_same_username(client, mock_user) -> None:
    """Testa se a rota de criação retorna erro quando username duplicado."""
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username já existe!'}


def test_create_user_same_email(client, mock_user) -> None:
    """Testa se a rota de criação retorna erro quando email duplicado."""
    response = client.post(
        '/users/',
        json={
            'username': 'teste_novo',
            'email': 'teste@teste.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'email já existe!'}


def test_read_users(client, mock_user, token) -> None:
    """Testa se a rota de leitura de usuários retorna a lista de usuários."""
    user_schema = UserPublic.model_validate(mock_user).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_id(client, mock_user, token) -> None:
    """Testa se a rota retorna o usuário pelo id."""
    response = client.get(
        f'/users/{mock_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'teste',
        'email': 'teste@teste.com',
    }


def test_read_user_id_error(client, mock_user, token) -> None:
    """Testa se a rota retorna 404 para usuário inexistente."""
    response = client.get(
        f'/users/{(mock_user.id) + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_update_user(client, mock_user, token) -> None:
    """Testa se a rota de atualização retorna o usuário atualizado."""
    response = client.put(
        f'/users/{mock_user.id}',
        json={
            'username': 'teste_novo',
            'email': 'teste_novo@teste.com',
            'password': '654321',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'teste_novo',
        'email': 'teste_novo@teste.com',
    }


def test_update_user_same_fields(client, mock_user, token) -> None:
    """Testa se atualizar usuário mantendo os mesmos campos é permitido."""
    # Cria um segundo usuário
    client.post(
        '/users/',
        json={
            'username': 'outro_usuario',
            'email': 'outro@teste.com',
            'password': '123456',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    # Tentativa de atualizar
    response = client.put(
        f'/users/{mock_user.id}',
        json={
            'username': 'outro_usuario',
            'email': 'teste@teste.com',
            'password': '123456',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'username ou email já existem!'}


def test_update_user_error(client, mock_user, token) -> None:
    """Testa se a rota retorna 403 ao tentar atualizar outro usuário."""
    response = client.put(
        f'/users/{(mock_user.id) + 1}',
        json={
            'username': 'teste_novo',
            'email': 'teste_novo@teste.com',
            'password': '654321',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para atualizar este usuário',
    }


def test_delete_user(client, mock_user, token) -> None:
    """Testa se a rota de remoção retorna o usuário removido."""
    response = client.delete(
        f'/users/{mock_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User delete'}


def test_delete_user_error(client, mock_user, token) -> None:
    """Testa se a rota retorna 403 ao tentar remover outro usuário."""
    response = client.delete(
        f'/users/{(mock_user.id) + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Você não tem permissão para remover este usuário',
    }
