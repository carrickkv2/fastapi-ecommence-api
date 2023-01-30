from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel


class Products(SQLModel, table=True):
    """
    Products table
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(unique=True, index=True)
    description: str
    image: str
    price: int
    currency: str
    discount: bool
    created_at: datetime = Field(default_factory=datetime.now)


class Users(SQLModel, table=True):
    """
    Users table
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    phone_number: str = Field(unique=True, index=True)
    first_name: str
    last_name: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now)


class OrderProducts(SQLModel, table=True):
    """
    Order products table.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    product_quantity: int = Field(default=1)
    order_id: int = Field(default=None, foreign_key="orders.id")
    created_at: datetime = Field(default_factory=datetime.now)


class Orders(SQLModel, table=True):
    """
    Orders table
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_phone: str = Field(foreign_key="users.phone_number")
    unique_reference_id: str = Field(unique=True, index=True)
    status: str = Field(default="pending")
    total_amount: int = Field()
    order_date: datetime = Field(default_factory=datetime.now)
    products: list["OrderProducts"] = Relationship()
