from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from catalogs.crud import get_product, create_product, list_products, get_category
from catalogs.models import Product


async def fetch_product_details(session: AsyncSession, product_id: int) -> Product:
    product = await get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
	return product



async def create_new_catalog_product(
    session: AsyncSession,
    name:str,
    price: Decimal,
    category_id: int,
    brand_id: int
    ) -> Product


	category = await get_category(session, category_id)
	if not category:
		raise HTTPException(status_code=404, detail="Категория не найдена")


	product = await create_product(
		session=session,
		name=name,
		price=price,
		category_id=category_id,
		brand_id=brand_id
	)
	return product
