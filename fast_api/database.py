"""Configuração da conexão e sessão do banco de dados."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.settings import Settings

# Cria a conexão com o database
engine = create_engine(Settings().DATABASE_URL)


def get_session():
    """Retorna uma sessão do banco de dados.

    Yields:
        Session: Sessão do SQLAlchemy para operações no banco de dados.

    """
    with Session(engine) as session:
        yield session
