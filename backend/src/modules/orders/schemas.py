
from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from .models import OrderStatus


class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    id: int
    cart_id: int



class CartRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    cart_items: CartItemRead


class OrderItemRead(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal


class OrderCreate(BaseModel):
    address: str


class OrderRead(BaseModel):
    id: int
    user_id: int
    address: str
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime

    order_items: List[OrderItemRead]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
