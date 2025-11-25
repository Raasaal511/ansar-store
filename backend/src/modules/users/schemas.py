from pydantic import BaseModel
from .models import UserRole


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    phone: str | None = None
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str | None
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdateStatus(BaseModel):
    is_active: bool

