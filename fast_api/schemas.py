"""Schemas Pydantic para validação e serialização da API."""

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    """Schema para a mensagem de boas-vindas."""

    message: str


class ErrorDetail(BaseModel):
    """Schema para resposta de erro (ex.: HTTPException)."""

    detail: str


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

    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    """Schema para persistência de usuário."""

    id: int


class UserList(BaseModel):
    """Schema para lista de usuários."""

    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
