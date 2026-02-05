from jwt import decode

from fast_api.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'teste': 'teste'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['teste'] == data['teste']
