"""Módulo principal da Fast API.

Este módulo contém a configuração principal da aplicação FastAPI
e as rotas da API.
"""

from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
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
def create_user(
    user: UserSchema, session: Session = Depends(get_session)
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

    user_db = User(**user.model_dump())
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


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
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )

    return user_db


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

    try:
        user_db.email = user.email
        user_db.username = user.username
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='username ou email já existem!',
        )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={404: {'model': ErrorDetail}},
)
def delete_user(
    user_id: int, session: Session = Depends(get_session)
) -> Message:
    """Remove um usuário pelo id e retorna o usuário removido."""
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    session.delete(user_db)
    session.commit()

    return Message(message='User delete')
