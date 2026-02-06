"""Módulo de segurança para hash e verificação de senhas."""

from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import User

# Pega um hash recomendado pela pwd
pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Provisório
SECRET_KEY = 'chave_secreta'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    """Gera o hash da senha usando o algoritmo recomendado."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Cria um token de acesso para validação."""
    # Faz uma copida dos dados para não alterar
    to_encode = data.copy()

    # Calcula o tempo de expiração
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Adiciona o campo 'exp' no payload
    to_encode.update({'exp': expire})

    # Monta o token
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    """Obtém o usuário atual a partir do token."""

    # Exceção para quando o token não é válido
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        # Decodifica o token
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        # Obtém o subject do token
        subject = payload.get('sub')
        # Se o subject não for encontrado, lança a exceção
        if not subject:
            raise credentials_exception
    # Se o token não for válido, lança a exceção
    except DecodeError:
        raise credentials_exception

    # Obtém o usuário do banco de dados
    user = session.scalar(select(User).where(User.email == subject))
    # Se o usuário não for encontrado, lança a exceção
    if not user:
        raise credentials_exception

    return user
