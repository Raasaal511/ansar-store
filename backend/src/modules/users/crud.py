from sqlalchemy.orm import Session
from .models import User, UserRole
from .services import hash_password

def create_user(db: Session, username: str,is_active: str, email: str, password: str, phone: str | None = None, role: UserRole = UserRole.USER) -> User:
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        phone=phone,
        password=hashed_password,
        role=role,
        is_active=is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()   

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False  
    db.delete(user)
    db.commit()
    return True 

def update_user_status(db: Session, user_id: int, is_active: bool) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user




