from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.src.db.database import get_session
from . import crud, schemas

router = APIRouter()


@router.post("/cart/items", response_model=schemas.CartItemRead)
def add_to_cart(
    user_id: int,
    item: schemas.CartItemCreate,
    db: Session = Depends(get_session),):

    item, created = crud.add_product_to_cart(db, user_id, item)

    if not created:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Товар уже находится в корзине")

    return item


@router.get("/cart", response_model=schemas.CartRead)
def get_cart(
    user_id: int,
    db: Session = Depends(get_session)):
    cart = crud.get_or_create_cart(db, user_id)
    return cart


@router.get("/cart/items", response_model=schemas.CartItemRead)
def get_cart_items(
    user_id: int,
    db: Session = Depends(get_session)):

    return crud.get_cart_items(db, user_id)


@router.delete("/cart/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)

def delete_cart_item(
    item_id: int,
    user_id: int,
    db: Session = Depends(get_session)):
    deleted = crud.delete_cart_item(db, user_id, item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Товар в корзине не найден")


@router.post("/orders", response_model=schemas.OrderRead)
def create_order(
    order_in: schemas.OrderCreate,
    user_id: int,
    db: Session = Depends(get_session)):

    order = crud.create_order_from_cart(db, user_id, order_in)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail ="Корзина пуста")
    return order


@router.get("/orders", response_model=schemas.OrderRead)
def get_orders(
    user_id: int,
    db: Session = Depends(get_session),):
    return crud.get_orders_for_user(db, user_id)


@router.get("/orders/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int,
    user_id: int,
    db: Session = Depends(get_session)):
    order = crud.get_order(db, order_id, user_id=user_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден")
    return order


@router.patch("/orders/{order_id}/status", response_model=schemas.OrderRead)
def change_order_status(
    order_id: int,
    statusss: schemas.OrderStatusUpdate,
    db: Session = Depends(get_session)):
    order = crud.update_order_status(db, order_id, statusss.status)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден")
    return order
