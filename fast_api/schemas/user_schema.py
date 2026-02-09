"""Schemas Pydantic para validação e serialização da API de usuários."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    """Schema para cadastro de usuário."""

    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    """Schema para exibição de usuário."""

    id: int
    username: str
    email: EmailStr

    # Configuração para serialização de atributos do modelo ORM
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    """Schema para lista de usuários."""

    users: list[UserPublic]
