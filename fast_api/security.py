"""Módulo de segurança para hash e verificação de senhas."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

# Pega um hash recomendado pela pwd
pwd_context = PasswordHash.recommended()

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
    """Cria um token de acesso para vaidação"""
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
