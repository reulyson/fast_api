"""Modelos ORM para a camada de persistência."""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Registry é um objeto que registra os modelos ORM
table_registry = registry()


# mapped_as_dataclass é um decorador que indica que o modelo é um dataclass
@table_registry.mapped_as_dataclass
class User:
    """Modelo ORM para usuários."""

    __tablename__ = 'users'

    # 'Mapped[tipo]' é um tipo de mapeamento
    # que indica que o atributo é uma coluna da tabela
    # 'mapped_column' é uma função que cria uma coluna na tabela
    # 'func.now' é uma função que retorna a data e hora atual
    # do servidor do banco de dados
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        # Define valor padrão na CRIAÇÃO (INSERT)
        server_default=func.now(),
        # Atualiza valor na MODIFICAÇÃO (UPDATE)
        onupdate=func.now(),
    )


@table_registry.mapped_as_dataclass
class Product:
    """Modelo ORM para produtos."""

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
