import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.common import generate_unique_reference_code
from ....core.common import get_current_user
from ....db import operations
from ....db.connect import get_session
from ....schemas.orders_endpoint_validators import OrderCreateSchema
from ....schemas.orders_endpoint_validators import OrderDB
from ....schemas.orders_endpoint_validators import OrderUpdateSchema
from ....schemas.orders_endpoint_validators import SpecificOrderSchema

log = logging.getLogger("uvicorn")
router = APIRouter()


@router.post("/create", response_model=OrderDB, status_code=201)
async def create_order(
    order: OrderCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to create an order using a POST request while ensuring that the
    order adheres to the specified schema.
    """

    for product in order.products:
        if await operations.get_product_by_id(session, product.product_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this id does not exist.",
            )

    if (
        await operations.get_user_by_email(session, order.email) is None
        or await operations.get_user_by_phone_number(session, order.phone_number) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to provide a valid email or a phone number.",
        )

    user = await operations.get_user_by_email(session, order.email)
    if user is not None:
        if user[0].email != order.email or user[0].phone_number != order.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not allowed to create an order for this user.",
            )

    try:

        order_products = [
            await operations.create_order_products(session, product.product_id, product.quantity)
            for product in order.products
        ]

        total_product_price = 0

        for product in order.products:
            product_price = await operations.get_product_price_by_id(session, product.product_id)
            total_product_price += product_price[0] * product.quantity

        current_order_dict = dict(order)
        current_order_dict["total_product_price"] = total_product_price
        current_order_dict["order_products"] = order_products
        current_order_dict["unique_reference_id"] = generate_unique_reference_code()

        db_response = await operations.add_order_to_db(session, current_order_dict)

        product_details = [
            await operations.get_product_by_id(session, product.product_id) for product in order.products
        ]

        final_product_details = []

        for i in range(len(product_details)):

            product = product_details[i][0]

            final_product_details.append(
                {
                    "product_id": product.id,
                    "product_image": product.image,
                    "currency": product.currency,
                    "product_title": product.title,
                    "product_description": product.description,
                    "product_price": product.price,
                }
            )

        for product in order.products:
            for product_detail in final_product_details:
                if product.product_id == product_detail["product_id"]:
                    product_detail["quantity"] = product.quantity

        response_object = {
            "order_id": db_response.id,
            "email": order.email,
            "phone_number": order.phone_number,
            "message": "Order created successfully",
            "total_amount": db_response.total_amount,
            "unique_reference_code": db_response.unique_reference_id,
            "status": db_response.status,
            "products": final_product_details,
            "date_created": db_response.order_date.strftime("%d-%m-%Y %H:%M:%S"),
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while creating the order.",
        )


@router.post("/get_specific_order/{id}", status_code=200)
async def get_specific_order(
    id: int,
    user_details: SpecificOrderSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to get a specific order from a customer using their order id.
    """
    if (
        await operations.get_user_by_email(session, user_details.email) is None
        or await operations.get_user_by_phone_number(session, user_details.phone_number) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or phone number does not exist.",
        )

    try:

        current_order = await operations.get_order_by_id(session, id)

        if current_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer has no orders with this id.",
            )

        current_order_products = await operations.get_order_products_by_order_id(session, id)

        product_details = []

        for i in range(len(current_order_products)):

            product = current_order_products[i]

            product_details.append(await operations.get_product_by_id(session, product[0].product_id))

        final_product_details = []

        for i in range(len(product_details)):

            product = product_details[i][0]

            final_product_details.append(
                {
                    "product_id": product.id,
                    "product_image": product.image,
                    "currency": product.currency,
                    "product_title": product.title,
                    "product_description": product.description,
                    "product_price": product.price,
                }
            )

        response_object = {
            "order_id": id,
            "email": user_details.email,
            "phone_number": user_details.phone_number,
            "total_amount": current_order[0].total_amount,
            "unique_reference_code": current_order[0].unique_reference_id,
            "products": final_product_details,
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while getting the order.",
        )


@router.post("/update/{id}", status_code=201)
async def update_order(
    id: int,
    order: OrderUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to update an order using a POST request.
    """

    for product in order.products:
        if await operations.get_product_by_id(session, product.product_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this id does not exist.",
            )

    if (
        await operations.get_user_by_email(session, order.email) is None
        or await operations.get_user_by_phone_number(session, order.phone_number) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to provide a valid email or a phone number.",
        )

    user = await operations.get_user_by_email(session, order.email)
    if user is not None:
        if user[0].email != order.email or user[0].phone_number != order.phone_number:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not allowed to update an order for this user.",
            )

    if await operations.get_order_by_phone_number(session, order.phone_number) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have an order.",
        )

    try:

        current_order = await operations.get_order_by_id(session, id)

        # order_products = [
        #     await operations.create_order_products(session, product.product_id, product.quantity)
        #     for product in order.products
        # ]

        total_product_price = 0

        for product in order.products:
            product_price = await operations.get_product_price_by_id(session, product.product_id)
            total_product_price += product_price[0] * product.quantity

        current_order_dict = dict(order)
        current_order_dict["total_product_price"] = total_product_price
        # current_order_dict["order_products"] = order_products

        db_response = await operations.update_order(session, current_order[0].id, current_order_dict)

        product_details = [
            await operations.get_product_by_id(session, product.product_id) for product in order.products
        ]

        final_product_details = []

        for i in range(len(product_details)):

            product = product_details[i][0]

            final_product_details.append(
                {
                    "product_id": product.id,
                    "product_image": product.image,
                    "currency": product.currency,
                    "product_title": product.title,
                    "product_description": product.description,
                    "product_price": product.price,
                }
            )

        for product in order.products:
            for product_detail in final_product_details:
                if product.product_id == product_detail["product_id"]:
                    product_detail["quantity"] = product.quantity

        response_object = {
            "order_id": db_response.id,
            "email": order.email,
            "phone_number": order.phone_number,
            "message": "Order updated successfully",
            "total_amount": db_response.total_amount,
            "unique_reference_code": db_response.unique_reference_id,
            "status": db_response.status,
            "products": final_product_details,
            "date_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while updating the order.",
        )
