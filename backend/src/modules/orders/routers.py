from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .models import OrderStatus

async def get_async_session() -> AsyncSession:
    raise RuntimeError("")

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: int
    line_total: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    address: str
    status: OrderStatus
    total_amount: int
    items: List[OrderItemOut]


class OrderCreateIn(BaseModel):
    address: str


class StatusPatchIn(BaseModel):
    status: OrderStatus