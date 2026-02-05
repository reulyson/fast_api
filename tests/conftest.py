"""Fixtures para os testes."""

from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.app import app
from fast_api.database import get_session
from fast_api.models import User, table_registry
from fast_api.security import get_password_hash


# Fixture para criar um cliente HTTP para testar a API
@pytest.fixture
def client(session):
    """Fixture para criar um cliente HTTP para testar a API."""

    # Arrange
    def get_session_overrides():
        """Função que retorna a sessão criada para teste."""
        return session

    with TestClient(app) as client:
        # troca a sessão prod para uma sessão test
        app.dependency_overrides[get_session] = get_session_overrides
        yield client
    # restaura as dependências originais da aplicação
    app.dependency_overrides.clear()


# Fixture para criar uma sessão de teste
@pytest.fixture
def session():
    """Fixture para criar uma sessão de teste."""
    # cria um motor de conexão com o banco de dados em memória
    engine = create_engine(
        # banco em memória, isolado por teste, sem arquivo
        'sqlite:///:memory:',
        # permite usar a conexão em outra thread
        #   (TestClient roda requisições em thread diferente da fixture)
        connect_args={'check_same_thread': False},
        # uma única conexão compartilhada para o banco em memória
        #   (evita múltiplos bancos vazios com :memory:)
        poolclass=StaticPool,
    )
    # cria todas as tabelas no banco de dados
    table_registry.metadata.create_all(engine)
    # cria uma sessão de teste
    with Session(engine) as session:
        # yield session é um gerador que retorna a sessão de teste
        yield session
    # deleta todas as tabelas no banco de dados
    table_registry.metadata.drop_all(engine)
    # Fecha as conexões abertas do SQLite e
    # desmonta o pool do engine de teste
    engine.dispose()


@contextmanager
def _mock_db_time(*, model: type, time: datetime):
    """Mocka o tempo do banco para o evento before_insert."""

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    def fake_update_hook(mapper, connection, target):
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    event.listen(model, 'before_update', fake_update_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)
    event.remove(model, 'before_update', fake_update_hook)


@pytest.fixture
def mock_db_time():
    """Fixture que retorna o context manager para mockar o tempo do banco."""
    return _mock_db_time


@pytest.fixture
def mock_user(session):
    """Cria um usuário de teste no banco de dados."""
    password = 'testeteste'
    user = User(
        username='teste',
        email='teste@teste.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # salva no objeto a senha de origem
    user.origin_password = password

    return user
