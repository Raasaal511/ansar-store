from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .crud import (
    create_notification,
    get_notification,
    get_user_notifications,
    update_notification,
    delete_notification
)
from .schemas import NotificationCreate, NotificationUpdate, NotificationResponse
from db.database import get_async_session


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationResponse)
async def create_notification_route(
    notification_data: NotificationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await create_notification(session, notification_data)


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification_route(
    notification_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    notification = await get_notification(session, notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    return notification


@router.get("/user/{user_id}", response_model=List[NotificationResponse])
async def get_user_notifications_route(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await get_user_notifications(session, user_id)


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification_route(
    notification_id: int,
    update_data: NotificationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    result = await update_notification(session, notification_id, update_data)
    if isinstance(result, str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result
        )
    return result


@router.delete("/{notification_id}")
async def delete_notification_route(
    notification_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    result = await delete_notification(session, notification_id)
    if isinstance(result, str) and "не найдено" in result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result
        )
    return {"message": result}