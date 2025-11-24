# catalogs/services.py
from decimal import Decimal
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from catalogs.crud import get_product, create_product, list_products, get_category, get_brand
from catalogs.models import Product


async def fetch_product_details(session: AsyncSession, product_id: int) -> Product:
    product = await get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


async def create_new_catalog_product(
    session: AsyncSession,
    name: str,
    price: Decimal,
    category_id: int,
    brand_id: int,
    description: str | None = None,
    characteristic: str | None = None,
    in_stock: bool = True,
    availability_count: int = 0,
) -> Product:
    category = await get_category(session, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")

    brand = await get_brand(session, brand_id)
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бренд не найден")

    product = await create_product(
        session=session,
        name=name,
        price=price,
        category_id=category_id,
        brand_id=brand_id,
        description=description,
        characteristic=characteristic,
        in_stock=in_stock,
        availability_count=availability_count,
    )
    return product
