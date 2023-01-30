from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import HttpUrl


class CreateProductSchema(BaseModel):
    """
    Pydantic validator (schema) for product creation.
    Defines a data validation model for the product create endpoint.
    This makes sure that we receive the data is what we expect.
    """

    class Config:
        extra = Extra.forbid  # forbid extra fields

    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    image: HttpUrl
    price: int
    currency: str
    discount: bool


class ProductDB(CreateProductSchema):
    product_id: int
    message: str

    class Config:
        orm_mode = True  # tell pydantic to read the data as if from an ORM, not a dict
