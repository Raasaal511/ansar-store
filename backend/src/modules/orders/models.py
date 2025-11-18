from datetime import datetime
from decimal import Decimal
import enum

from backend.src.db.database import Base
from sqlalchemy import (
    DateTime, Enum, ForeignKey,
    DECIMAL, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderStatus(str, enum.Enum):
    accepted = "принят"
    delivery = "доставляется"
    delivered = "доставлено"
    cancel = "отменено"


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(int, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"), nullable=False)
    
    product_id: Mapped[int] = mapped_column(int, nullable=False)
    quantity: Mapped[int] = mapped_column(int, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL('0.00'), nullable=False)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(int, nullable=False)
    address: Mapped[str] = mapped_column(str(255), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL('0.00'),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False)
    
    product_id: Mapped[int] = mapped_column(int, nullable=False)
    quantity: Mapped[int] = mapped_column(int, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL('0.00'), nullable=False)
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")
