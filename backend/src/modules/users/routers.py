from db.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..users import crud
from ..users.models import User, UserRole
from ..users.schemas import UserCreate, UserResponse, UserUpdateStatus


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    existing_user = await crud.get_user_by_username(db, user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = await crud.get_user_by_email(db, user_create.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = await crud.create_user(
        db,
        username=user_create.username,
        email=user_create.email,
        password=user_create.password,
        phone=user_create.phone,
        role=user_create.role
    )
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_async_session)
):
    users = await crud.get_all_users(db)
    return users

@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_user_status(
    user_id: int,
    status_update: UserUpdateStatus,
    db: AsyncSession = Depends(get_async_session)
):
    user = await crud.update_user_status(db, user_id, status_update.is_active)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    success = await crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

