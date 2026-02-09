"""Schemas Pydantic para validação e serialização da API."""

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Schema para a mensagem de boas-vindas."""

    message: str


class ErrorDetail(BaseModel):
    """Schema para resposta de erro (ex.: HTTPException)."""

    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterParams(BaseModel):
    limit: int = Field(default=10, ge=1)
    offset: int = Field(default=0, ge=0)
