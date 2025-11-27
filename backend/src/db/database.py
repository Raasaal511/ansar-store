from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings.settings import settings



async_engine = create_async_engine(
    url=settings.database_url,
    echo=False,
)

session_local = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает асинхронную сессию для работы с БД."""
    async with session_local() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase, AsyncAttrs):
    """Базовый класс для всех моделей проекта."""
    pass



