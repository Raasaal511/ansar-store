from passlib import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from .env import get_auth_data
from .env import SECRET_KEY, ALGORITHM
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .jwt_utils import create_access_token, verify_token
from users.models import User
from sqlalchemy.orm import Session  
from database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> User:     
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("email")


        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token: no email")


    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


    user = db.query(User).filter(User.email == user_email).first()


    if user is None:
        raise HTTPException(status_code=404, detail="User not found")


    return user