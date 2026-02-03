"""Testes para a camada de persistência (modelos e banco de dados)."""

from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from fast_api.models import User


def test_create_user(session, mock_db_time) -> None:
    """Testa se o usuário é criado com sucesso."""
    # mocka o tempo do banco de dados
    with mock_db_time(model=User, time=datetime(2026, 1, 1)) as time:
        new_user = User(
            username='teste',
            email='teste@teste.com',
            password='123456',
        )
        # add: adiciona o usuário na sessão
        session.add(new_user)
        # commit: confirma as alterações na sessão
        # e salva no banco de dados
        session.commit()

        # scalar: faz uma consulta e retorna o primeiro resultado da consulta
        user = session.scalar(select(User).where(User.username == 'teste'))

        # verifica se os valores são os esperados
        assert asdict(user) == {
            'id': 1,
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': '123456',
            'created_at': time,
            'updated_at': time,
        }
