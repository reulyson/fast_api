from http import HTTPStatus

from fast_api.schemas.product_schema import ProductPublic


def test_create_product(client, token) -> None:
    """Testa se a rota de criação de produto retorna o produto criado."""
    response = client.post(
        '/products/',
        json={
            'name': 'produto_teste',
            'description': 'descrição_teste',
            'price': 100.00,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'produto_teste',
        'description': 'descrição_teste',
        'price': 100.00,
    }


def test_existing_product(client, token, mock_product) -> None:
    """Testa se a rota de criação retorna erro quando o produto já existe."""
    response = client.post(
        '/products/',
        json={
            'name': mock_product.name,
            'description': mock_product.description,
            'price': mock_product.price,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Produto já existe!'}


def test_read_products(client, token, mock_product) -> None:
    """Testa se a rota de leitura de produtos retorna todos os produtos."""
    product_schema = ProductPublic.model_validate(mock_product).model_dump()
    response = client.get(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'products': [product_schema]}


def test_read_product_id(client, token, mock_product) -> None:
    """Testa se a rota de leitura de produto retorna o produto pelo id."""
    product_schema = ProductPublic.model_validate(mock_product).model_dump()
    response = client.get(
        f'/products/{mock_product.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == product_schema


def test_not_found_product_id(client, token, mock_product) -> None:
    """Testa se a rota retorna 404 para produto inexistente."""
    response = client.get(
        f'/products/{mock_product.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Produto não encontrado!'}


def test_update_product(client, token, mock_product) -> None:
    """Testa se a rota de atualização de produto funciona corretamente."""
    response = client.put(
        f'/products/{mock_product.id}',
        json={
            'name': 'produto_teste_atualizado',
            'description': 'descrição_teste_atualizada',
            'price': 100.00,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': mock_product.id,
        'name': 'produto_teste_atualizado',
        'description': 'descrição_teste_atualizada',
        'price': 100.00,
    }


def test_update_product_not_found(client, token, mock_product) -> None:
    """Testa se a rota retorna 404 para produto inexistente."""
    response = client.put(
        f'/products/{mock_product.id + 1}',
        json={
            'name': 'produto_teste_atualizado',
            'description': 'descrição_teste_atualizada',
            'price': 100.00,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Produto não encontrado!'}


def test_update_product_existing(client, token, mock_product) -> None:
    """Testa se a rota retorna 409 para nome de produto já existente."""
    client.post(
        '/products/',
        json={
            'name': 'produto_teste_existente',
            'description': 'descrição_teste_existente',
            'price': 100.00,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    response = client.put(
        f'/products/{mock_product.id}',
        json={
            'name': 'produto_teste_existente',
            'description': mock_product.description,
            'price': mock_product.price,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nome de produto já existe!'}


def test_delete_product(client, token, mock_product) -> None:
    """Testa se a rota de deleção de produto funciona corretamente."""
    response = client.delete(
        f'/products/{mock_product.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Produto deletado!'}


def test_delete_product_not_found(client, token, mock_product) -> None:
    """Testa se a rota retorna 404 para produto inexistente."""
    response = client.delete(
        f'/products/{mock_product.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Produto não encontrado!'}
