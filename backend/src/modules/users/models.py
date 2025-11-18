from enum import Enum

from sqlalchemy import String, Integer, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from db.database import Base


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"
    MANAGER = "manager"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
