"""Configuração da conexão e sessão do banco de dados."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_api.settings import Settings

# Cria a conexão com o database
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    """Retorna uma sessão do banco de dados.

    Yields:
        AsyncSession: Sessão do SQLAlchemy para operações no banco de dados.

    """
    # Cria um sessão assíncrona com o motor de conexão,
    # não expira as entidades ao commitar a transação
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # Yield: Retorna a sessão assíncrona
        yield session
