from datetime import datetime
import enum

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
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship





class OrderStatus(str, enum.Enum):
    pending = "создан, ожидает оплаты"
    paid = "плачен"
    shipped = "передан в доставку"
    completed = "завершён"
    cancelled = "отменён"


class Cart(Base):
    pass

class CartItem(Base):
    pass

class Order(Base):
    pass