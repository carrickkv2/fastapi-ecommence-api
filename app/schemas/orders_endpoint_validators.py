from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class Products(BaseModel):
    """
    Pydantic validator (schema) for products added to an order.
    """

    product_id: int
    quantity: int
    product_title: str | None
    product_description: str | None
    product_image: str | None
    currency: str | None
    product_price: int | None


class OrderCreateSchema(BaseModel):
    """
    Pydantic validator (schema) for order creation.
    Defines a data validation model for order create endpoint.
    This makes sure that we receive the data is what we expect.
    """

    class Config:
        extra = Extra.forbid  # forbid extra fields

    email: str
    phone_number: str
    products: list[Products]


class OrderUpdateSchema(OrderCreateSchema):
    ...


class OrderDB(OrderCreateSchema):
    order_id: int
    total_amount: int
    unique_reference_code: str
    status: str
    message: str
    date_created: str

    class Config:
        orm_mode = True  # tell pydantic to read the data as if from an ORM, not a dict


class SpecificOrderSchema(BaseModel):
    email: str
    phone_number: str

    class Config:
        extra = Extra.forbid  # forbid extra fields
