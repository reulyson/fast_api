"""Schemas Pydantic para validação e serialização da API de produtos."""

from pydantic import BaseModel, ConfigDict


class ProductSchema(BaseModel):
    """Schema para cadastro de produto."""

    name: str
    description: str
    price: float


class ProductPublic(BaseModel):
    """Schema para exibição de produto."""

    id: int
    name: str
    description: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    """Schema para lista de produtos."""

    products: list[ProductPublic]
