from typing import List, Optional
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from catalogs.models import Product, Category, Brand

async def get_product(session: AsyncSession, product_id: int) -> Optional[Product]:
    stmt = select(Product).where(Product.id == product_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_product(
    session: AsyncSession,
    name: str,
    price: Decimal,
    category_id: int,
    brand_id: int,
    description: Optional[str] = None,
    characteristic: Optional[str] = None,
    in_stock: bool = True,
    availability_count: int = 0,
) -> Product:
    new_product = Product(
        name=name,
        price=price,
        category_id=category_id,
        brand_id=brand_id,
        description=description,
        characteristic=characteristic,
        in_stock=in_stock,
        availability_count=availability_count,
    )
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def list_products(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
    stmt = select(Product).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_category(session: AsyncSession, category_id: int) -> Optional[Category]:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_brand(session: AsyncSession, brand_id: int) -> Optional[Brand]:
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
