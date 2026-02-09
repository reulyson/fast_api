from http import HTTPStatus

from jwt import decode

from fast_api.security import create_access_token
from fast_api.settings import Settings


def test_jwt():
    """Testa se o token JWT é criado corretamente."""
    data = {'teste': 'teste'}
    token = create_access_token(data)

    settings = Settings()
    decoded = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert decoded['teste'] == data['teste']


def test_jwt_invalid_token(client):
    """Testa se o token JWT é inválido."""
    token = 'invalid_token'
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_subject_not_found(client):
    """Testa se o subject não for enviado no token."""
    token = create_access_token({})
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_user_not_found(client):
    """Testa se o usuário não for encontrado no banco de dados."""
    token = create_access_token({'sub': 'error@teste.com'})
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
