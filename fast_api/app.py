"""Módulo principal da Fast API.

Este módulo contém a configuração principal da aplicação FastAPI
e as rotas da API.
"""

from http import HTTPStatus

from fastapi import FastAPI

from fast_api.routers import auth, users
from fast_api.schemas import Message

app = FastAPI(
    title='Fast API',
    description='API desenvolvida com FastAPI',
    version='0.1.0',
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root() -> Message:
    """Retorna uma mensagem de boas-vindas."""
    return {'message': 'Hello, World!'}
