# catalogs/routers.py
from typing import List
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_async_session
from users.depends import role_deps  # <-- зависимость пользователей (как просил)

from catalogs.models import Product
from catalogs.services import fetch_product_details, create_new_catalog_product
from catalogs.crud import list_products

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


class ProductBase(BaseModel):
    name: str
    price: Decimal
    category_id: int
    brand_id: int
    description: str | None = None
    characteristic: str | None = None
    in_stock: bool = True
    availability_count: int = 0

    class Config:
        orm_mode = True  


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


@router.get(
    "/",
    response_model=List[ProductRead],
    dependencies=[role_deps("admin", "manager", "user")]
)
async def read_products(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    products = await list_products(session, skip=skip, limit=limit)
    return products


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[role_deps("admin")]  
)
async def create_product_endpoint(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_product = await create_new_catalog_product(
        session=session,
        name=product_data.name,
        price=product_data.price,
        category_id=product_data.category_id,
        brand_id=product_data.brand_id,
        description=product_data.description,
        characteristic=product_data.characteristic,
        in_stock=product_data.in_stock,
        availability_count=product_data.availability_count,
    )
    return new_product


@router.get(
    "/{product_id}",
    response_model=ProductRead,
    dependencies=[role_deps("admin", "manager", "user")]
)
async def read_product_details(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    product = await fetch_product_details(session, product_id)
    return product
