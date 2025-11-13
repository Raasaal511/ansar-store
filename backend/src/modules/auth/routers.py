from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .jwt_utils import create_access_token, verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


fake_db = {
    "user@example.com": {
        "username": "user@example.com",
        "password": "1234"
    }
}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return {"user": payload.get("sub")}