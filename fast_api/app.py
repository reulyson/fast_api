"""Módulo principal da Fast API.

Este módulo contém a configuração principal da aplicação FastAPI
e as rotas da API.
"""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_api.schemas import (
    ErrorDetail,
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(
    title='Fast API',
    description='API desenvolvida com FastAPI',
    version='0.1.0',
)

database = []


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
)
def create_user(user: UserSchema) -> UserPublic:
    """Cria um novo usuário."""
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users() -> UserList:
    """Retorna todos os usuários."""
    return {'users': database}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def read_user_id(user_id: int) -> UserPublic:
    """Retorna um usuário pelo id."""
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )
    return database[user_id - 1]


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def update_user(user_id: int, user: UserSchema) -> UserPublic:
    """Atualiza um usuário existente pelo id."""
    user_with_id = UserDB(id=user_id, **user.model_dump())

    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
    responses={404: {'model': ErrorDetail}},
)
def delete_user(user_id: int) -> UserPublic:
    """Remove um usuário pelo id e retorna o usuário removido."""
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
        )
    return database.pop(user_id - 1)
