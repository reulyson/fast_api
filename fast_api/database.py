from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.settings import Settings

# Cria a conexão com o database
engine = create_engine(Settings().DATABASE_URL)


def get_session():
    # Inicia a sessão do banco
    with Session(engine) as session:
        yield session
