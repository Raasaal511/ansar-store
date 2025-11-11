from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

async_engine = create_async_engine(url=DATABASE_URL)
session_local = async_sessionmaker(bind=async_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_local() as session:
        try:
            yield session
        finally:
            await session.close()


class Base(DeclarativeBase, AsyncAttrs):
    pass



