from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import Notification as model_notif
from .schemas import NotificationCreate, NotificationUpdate



async def create_notification(
    session: AsyncSession, 
    notification_data: NotificationCreate
):
    db_notif = model_notif(
        user_id=notification_data.user_id,
        message=notification_data.message,
        status=notification_data.status
    )
    session.add(db_notif)
    await session.commit()
    await session.refresh(db_notif)
    return db_notif



async def get_notification(
    session: AsyncSession, 
    notification_id: int
):
    result = await session.execute(
        select(model_notif).where(model_notif.id == notification_id)
    )
    return result.scalar_one_or_none()



async def get_user_notifications(
    session: AsyncSession, 
    user_id: int
):
    result = await session.execute(
        select(model_notif).where(model_notif.user_id == user_id)
    )
    return list(result.scalars().all())




async def update_notification(
    session: AsyncSession,
    notification_id: int,
    update_data: NotificationUpdate
):
    result = await session.execute(
        select(model_notif).where(model_notif.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        return None

    if update_data.message is not None:
        notification.message = update_data.message
    if update_data.status is not None:
        notification.status = update_data.status
        
    await session.commit()
    await session.refresh(notification)
    return notification

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from .models import Notification as model_notif
from .schemas import NotificationCreate, NotificationUpdate

async def create_notification(
    session: AsyncSession, 
    notification_data: NotificationCreate
):
    db_notif = model_notif(
        user_id=notification_data.user_id,
        message=notification_data.message,
        status=notification_data.status
    )
    session.add(db_notif)
    await session.commit()
    await session.refresh(db_notif)
    return db_notif

async def get_notification(
    session: AsyncSession, 
    notification_id: int
):
    result = await session.execute(
        select(model_notif).where(model_notif.id == notification_id)
    )
    return result.scalar_one_or_none()

async def get_user_notifications(
    session: AsyncSession, 
    user_id: int
):
    result = await session.execute(
        select(model_notif).where(model_notif.user_id == user_id)
    )
    return list(result.scalars().all())

async def update_notification(
    session: AsyncSession,
    notification_id: int,
    update_data: NotificationUpdate
):
    result = await session.execute(
        select(model_notif).where(model_notif.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        return "Уведомление не найдено"

    if update_data.message is not None:
        notification.message = update_data.message
    if update_data.status is not None:
        notification.status = update_data.status
        
    await session.commit()
    await session.refresh(notification)
    return notification

async def delete_notification(
    session: AsyncSession, 
    notification_id: int
):
    result = await session.execute(
        select(model_notif).where(model_notif.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        return "Уведомление не найдено"
        
    await session.delete(notification)
    await session.commit()
    return "Уведомление удалено"