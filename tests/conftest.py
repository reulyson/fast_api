"""Fixtures para os testes."""

from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_api.app import app
from fast_api.models import table_registry


# Fixture para criar um cliente HTTP para testar a API
@pytest.fixture
def client() -> TestClient:
    """Fixture para criar um cliente HTTP para testar a API."""
    # Arrange
    return TestClient(app)


# Fixture para criar uma sessão de teste
@pytest.fixture
def session() -> Generator[Session, None, None]:
    """Fixture para criar uma sessão de teste."""
    # cria um motor de conexão com o banco de dados em memória
    engine = create_engine('sqlite:///:memory:')
    # cria todas as tabelas no banco de dados
    table_registry.metadata.create_all(engine)
    # cria uma sessão de teste
    with Session(engine) as session:
        # yield session é um gerador que retorna a sessão de teste
        yield session
    # deleta todas as tabelas no banco de dados
    table_registry.metadata.drop_all(engine)


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
