from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User, UserRole


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    phone: str | None = None,
    role: UserRole = UserRole.USER
) -> User:
    """Создать нового пользователя (пароль уже должен быть хешированным!)"""
    new_user = User(
        username=username,
        email=email,
        phone=phone,
        password=password,  # Пароль приходит уже хешированным из routers
        role=role,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Получить пользователя по username"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Получить пользователя по email"""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """Получить пользователя по ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_all_users(db: AsyncSession) -> list[User]:
    """Получить всех пользователей"""
    result = await db.execute(select(User))
    return list(result.scalars().all())


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """Удалить пользователя"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return False
    
    await db.delete(user)
    await db.commit()
    return True


async def update_user_status(db: AsyncSession, user_id: int, is_active: bool) -> User | None:
    """Обновить статус пользователя"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return user
