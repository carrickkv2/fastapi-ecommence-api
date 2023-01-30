from fastapi import APIRouter

from .endpoints import auth
from .endpoints import orders
from .endpoints import products


api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
