from datetime import datetime
import enum

from backend.src.db.database import Base
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderStatus(str, enum.Enum):

    pending = "ожидает оплаты"
    paid = "оплачен"
    shipped = "отгружен"
    completed = "завершён"
    cancelled = "отменён"


class Cart(Base):

    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)                      
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)     
    created_at: Mapped[datetime] = mapped_column(                         
        DateTime(timezone=True), server_default=func.now(), nullable=False)

    items: Mapped[list["CartItem"]] = relationship()


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="cartitem_post"),           
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"))

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)          


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)         
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"), default=OrderStatus.pending, nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    items: Mapped[list["OrderItem"]] = relationship()


class OrderItem(Base):

    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="orderitem_post"))

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)              
    line_total: Mapped[int] = mapped_column(Integer, nullable=False)              
