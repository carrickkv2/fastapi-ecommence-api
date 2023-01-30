import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.common import get_current_user
from ....db import operations
from ....db.connect import get_session
from ....schemas.product_endpoint_validators import CreateProductSchema
from ....schemas.product_endpoint_validators import ProductDB

log = logging.getLogger("uvicorn")
router = APIRouter()


@router.post(
    "/create",
    response_model=ProductDB,
    status_code=201,
)
async def create_product(
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    """
    An endpoint to create a single product using a POST request while ensuring that the
    order adheres to the specified schema.
    """

    if await operations.get_product_by_title(session, product.title) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product with this title already exists.",
        )

    try:

        db_response = await operations.add_product_to_db(session, product)
        db_response = dict(db_response)

        response_object = {
            "product_id": db_response["id"],
            "message": "Product created successfully",
            "title": product.title,
            "description": product.description,
            "image": product.image,
            "price": product.price,
            "currency": product.currency,
            "discount": product.discount,
        }

        return response_object

    except Exception as e:
        log.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error : [ {e} ] occurred while creating the product.",
        )
