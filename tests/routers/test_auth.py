from http import HTTPStatus

from fast_api.security import create_access_token


def test_create_token(client, mock_user):
    """Testa se o token é criado corretamente."""
    response = client.post(
        '/auth/',
        data={
            'username': mock_user.email,
            'password': mock_user.origin_password,
        },
    )

    assert response.status_code == HTTPStatus.OK
    access_token = create_access_token({'sub': mock_user.email})
    assert response.json() == {
        'access_token': access_token,
        'token_type': 'Bearer',
    }


def test_create_token_error_username(client, mock_user):
    """Testa se o token é criado corretamente."""
    response = client.post(
        '/auth/',
        data={
            'username': 'error@teste.com',
            'password': mock_user.origin_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_create_token_error_password(client, mock_user):
    """Testa se o token é criado corretamente."""
    response = client.post(
        '/auth/',
        data={
            'username': mock_user.email,
            'password': 'senha_error',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Senha incorreta'}
