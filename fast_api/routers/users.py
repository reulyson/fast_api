from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterParams = Annotated[FilterParams, Query()]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    responses={409: {'model': ErrorDetail}},
)
def create_user(
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
) -> UserPublic:
    """Cria um novo usuário."""
    existing_user: User | None = session.scalar(
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
    session.commit()
    session.refresh(user_db)

    return user_db


@router.get('/', status_code=HTTPStatus.OK)
def read_users(
    filter_params: FilterParams,
    session: Session,
    current_user: CurrentUser,
) -> UserList:
    """Retorna todos os usuários."""
    users = session.scalars(
        select(User).limit(filter_params.limit).offset(filter_params.offset)
    )
    return {'users': users}


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    responses={404: {'model': ErrorDetail}},
)
def read_user_id(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
) -> UserPublic:
    """Retorna um usuário pelo id."""
    user_db = session.scalar(select(User).where(User.id == user_id))

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
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
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
        session.commit()
        # Refresca o usuário atualizado
        session.refresh(current_user)

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
def delete_user(
    user_id: int,
    session: Session,
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
    session.delete(current_user)
    session.commit()

    return Message(message='User delete')
