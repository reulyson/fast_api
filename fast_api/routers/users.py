from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import (
    ErrorDetail,
    FilterParams,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_api.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

# Dependencies Annotated
AsyncSession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterParams = Annotated[FilterParams, Query()]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    responses={409: {'model': ErrorDetail}},
)
async def create_user(
    user: UserSchema,
    session: AsyncSession,
    current_user: CurrentUser,
) -> UserPublic:
    """Cria um novo usuário."""
    existing_user: User | None = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='username já existe!'
            )
        elif existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='email já existe!'
            )

    user_db = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)

    return user_db


@router.get('/', status_code=HTTPStatus.OK)
async def read_users(
    filter_params: FilterParams,
    session: AsyncSession,
    current_user: CurrentUser,
) -> UserList:
    """Retorna todos os usuários."""
    users = await session.scalars(
        select(User).limit(filter_params.limit).offset(filter_params.offset)
    )
    return {'users': users}


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def read_user_id(
    user_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
) -> UserPublic:
    """Retorna um usuário pelo id."""
    user_db = await session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )

    return user_db


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: AsyncSession,
    current_user: CurrentUser,
) -> UserPublic:
    """Atualiza um usuário existente pelo id."""
    # Verifica se o usuário atual é o mesmo que está sendo atualizado
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )
    # Tenta atualizar o usuário
    try:
        current_user.email = user.email
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        # Adiciona o usuário atualizado ao banco de dados
        session.add(current_user)
        # Commita a transação
        await session.commit()
        # Refresca o usuário atualizado
        await session.refresh(current_user)

        return current_user
    # Se o usuário já existir, lança uma exceção
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='username ou email já existem!',
        )


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
async def delete_user(
    user_id: int,
    session: AsyncSession,
    current_user: CurrentUser,
) -> Message:
    """Remove um usuário pelo id e retorna o usuário removido."""

    # Verifica se o usuário atual é o mesmo que está sendo removido
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para remover este usuário',
        )
    # Remove o usuário
    await session.delete(current_user)
    await session.commit()

    return Message(message='User delete')
