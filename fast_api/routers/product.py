from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database import get_session
from fast_api.models import Product, User
from fast_api.schemas.product_schema import (
    ProductList,
    ProductPublic,
    ProductSchema,
)
from fast_api.schemas.schemas import ErrorDetail, FilterParams, Message
from fast_api.security import get_current_user

router = APIRouter(prefix='/products', tags=['products'])

# Dependencies Annotated
AsyncSession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterParams = Annotated[FilterParams, Query()]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    responses={409: {'model': ErrorDetail}},
)
async def create_product(
    product: ProductSchema,
    session: AsyncSession,
    current_user: CurrentUser,
) -> ProductPublic:
    """Cria um novo produto."""
    existing_product: Product | None = await session.scalar(
        select(Product).where(Product.name == product.name)
    )
    if existing_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Produto já existe!'
        )
    product_db = Product(
        name=product.name,
        description=product.description,
        price=product.price,
    )
    session.add(product_db)
    await session.commit()
    await session.refresh(product_db)
    return product_db


@router.get(
    '/', status_code=HTTPStatus.OK, responses={404: {'model': ErrorDetail}}
)
async def read_products(
    session: AsyncSession,
    filter_params: FilterParams,
    current_user: CurrentUser,
) -> ProductList:
    """Retorna todos os produtos."""
    products = await session.scalars(
        select(Product).limit(filter_params.limit).offset(filter_params.offset)
    )
    return ProductList(products=products)


@router.get(
    '/{product_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def read_product_id(
    product_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
) -> ProductPublic:
    """Retorna um produto pelo id."""
    product_db = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado!'
        )
    return product_db


@router.put(
    '/{product_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def update_product(
    product_id: int,
    product: ProductSchema,
    session: AsyncSession,
    current_user: CurrentUser,
) -> ProductPublic:
    """Atualiza um produto existente pelo id."""
    product_db = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado!'
        )

    existing_product: Product | None = await session.scalar(
        select(Product).where(Product.name == product.name)
    )
    if existing_product:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de produto já existe!',
        )
    product_db.name = product.name
    product_db.description = product.description
    product_db.price = product.price

    session.add(product_db)
    await session.commit()
    await session.refresh(product_db)

    return product_db


@router.delete(
    '/{product_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def delete_product(
    product_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
) -> Message:
    """Deleta um produto existente pelo id."""
    product_db = await session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto não encontrado!'
        )
    await session.delete(product_db)
    await session.commit()
    return Message(message='Produto deletado!')
