from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..schemas.auth_endpoint_validators import UserSignupSchema
from ..schemas.product_endpoint_validators import CreateProductSchema
from .models import OrderProducts
from .models import Orders
from .models import Products
from .models import Users


async def add_product_to_db(db_session: AsyncSession, payload: CreateProductSchema):
    product = Products(
        title=payload.title,
        description=payload.description,
        image=payload.image,
        price=payload.price,
        currency=payload.currency,
        discount=payload.discount,
    )
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    return product


async def get_all_products(db_session: AsyncSession):
    query = select(Products)
    results = await db_session.execute(query)
    return results.all()


async def get_product_by_title(db_session: AsyncSession, title: str):
    query = select(Products).where(Products.title == title)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_product_by_id(db_session: AsyncSession, id: int):
    query = select(Products).where(Products.id == id)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_product_price_by_id(db_session: AsyncSession, id: int):
    query = select(Products.price).where(Products.id == id)
    results = await db_session.execute(query)
    return results.one_or_none()


async def add_new_user_to_db(db_session: AsyncSession, payload: UserSignupSchema):
    user = Users(
        email=payload.email,
        password=payload.password,
        phone_number=payload.phone_number,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def get_user_by_email(db_session: AsyncSession, email: str):
    query = select(Users).where(Users.email == email)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_user_by_phone_number(db_session: AsyncSession, phone_number: str):
    query = select(Users).where(Users.phone_number == phone_number)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_user_by_id(db_session: AsyncSession, id: int):
    query = select(Users).where(Users.id == id)
    results = await db_session.execute(query)
    return results.one_or_none()


async def create_order_products(db_session: AsyncSession, product_id: int, product_quantity: int):
    order_products = OrderProducts(
        product_id=product_id,
        product_quantity=product_quantity,
    )
    db_session.add(order_products)
    await db_session.commit()
    await db_session.refresh(order_products)
    return order_products


async def add_order_to_db(db_session: AsyncSession, payload: dict):
    order = Orders(
        customer_phone=payload["phone_number"],
        status="success",
        total_amount=payload["total_product_price"],
        products=payload["order_products"],
        unique_reference_id=payload["unique_reference_id"],
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    return order


async def get_order_products_by_order_id(db_session: AsyncSession, order_id: int):
    query = select(OrderProducts).where(OrderProducts.order_id == order_id)
    results = await db_session.execute(query)
    return results.all()


async def get_order_by_phone_number(db_session: AsyncSession, phone_number: str):
    query = select(Orders).where(Orders.customer_phone == phone_number)
    results = await db_session.execute(query)
    return results.all()


async def get_order_by_unique_reference_id(db_session: AsyncSession, unique_reference_id: str):
    query = select(Orders).where(Orders.unique_reference_id == unique_reference_id)
    results = await db_session.execute(query)
    return results.one_or_none()


async def get_order_by_id(db_session: AsyncSession, order_id: int):
    query = select(Orders).where(Orders.id == order_id)
    results = await db_session.execute(query)
    return results.one_or_none()


async def update_order(db_session: AsyncSession, order_id: int, payload: dict):
    query = select(Orders).where(Orders.id == order_id)
    results = await db_session.execute(query)
    order = results.one()
    # order[0].products = payload["order_products"]
    order[0].total_amount = payload["total_product_price"]
    db_session.add(order[0])
    await db_session.commit()
    await db_session.refresh(order[0])
    return order[0]
