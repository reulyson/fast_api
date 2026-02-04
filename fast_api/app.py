"""Módulo principal da Fast API.

Este módulo contém a configuração principal da aplicação FastAPI
e as rotas da API.
"""

from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import (
    ErrorDetail,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(
    title='Fast API',
    description='API desenvolvida com FastAPI',
    version='0.1.0',
)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root() -> Message:
    """Retorna uma mensagem de boas-vindas."""
    return {'message': 'Hello, World!'}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    responses={409: {'model': ErrorDetail}},
)
def create_user(user: UserSchema, session=Depends(get_session)) -> UserPublic:
    """Cria um novo usuário."""

    db_user: User | None = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    # Retorna Error
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='username já existe!'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='email já existe!'
            )

    new_user = User(**user.model_dump())
    # Registra o obj na sessão
    session.add(new_user)
    # Envia de fato para o database
    session.commit()
    # Atualiza o obj em relação ao database
    session.refresh(new_user)

    return new_user


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
) -> UserList:
    """Retorna todos os usuários."""
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def read_user_id(
    user_id: int, session: Session = Depends(get_session)
) -> UserPublic:
    """Retorna um usuário pelo id."""
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )

    user = session.scalar(select(User).where(User.id == user_id))
    return user


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
) -> UserPublic:
    """Atualiza um usuário existente pelo id."""
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    user_db.email = user.email
    user_db.username = user.username
    user_db.password = user.password

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def delete_user(
    user_id: int, session: Session = Depends(get_session)
) -> UserPublic:
    """Remove um usuário pelo id e retorna o usuário removido."""
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    session.delete(user_db)
    session.commit()

    return user_db
