from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database import get_session
from fast_api.models import User
from fast_api.schemas import Token
from fast_api.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])
# Dependencies Annotated
AsyncSession = Annotated[AsyncSession, Depends(get_session)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/', response_model=Token)
async def login_for_access_token(
    form_data: OAuthForm,
    session: AsyncSession,
):
    user_db = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretos',
        )

    # Verifica se a senha passada está cadastrada
    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Senha incorreta'
        )

    access_token = create_access_token({'sub': user_db.email})

    return Token(access_token=access_token, token_type='Bearer')
