from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import User, UserRole
from auth.services import hash_password


async def create_user(db: AsyncSession, username: str, is_active: str, email: str, password: str, phone: str | None = None, role: UserRole = UserRole.USER) -> User:
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        phone=phone,
        password=hashed_password,
        role=role,
        is_active=is_active
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(
        select(User)
        .where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HttpException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result =  await db.execute(
        select(User)
        .where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HttpException(status_code=404, detail="User not found")
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result =  await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HttpException(status_code=404, detail="User not found")
    return user


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
    

async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await db.execute(
        db.query(User).filter(User.id == user_id)
    ).scalar_one_or_none()
    if not user:
        return False  
    await db.delete(user)
    await db.commit()


async def update_user_status(db: AsyncSession, user_id: int, is_active: bool) -> User | None:
    user = await db.execute(
        db.query(User).filter(User.id == user_id)
    ).scalar_one_or_none()
    if not user:
        return None  
    user.is_active = is_active
    await db.commit()
    await db.refresh(user)
    return user
