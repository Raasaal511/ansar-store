from decimal import Decimal
from sqlalchemy.orm import Session
from backend.src.modules.orders import models, schemas


def get_create_cart(db: Session, user_id: int) -> models.Cart:
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if cart is None:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def get_cart_items(db: Session, user_id: int) -> list[models.CartItem]:
    cart = get_create_cart(db, user_id)
    return cart.cart_items


def add_product_to_cart(
    db: Session,
    user_id: int,
    item: schemas.CartItemCreate) -> tuple[models.CartItem, bool]:

    cart = get_create_cart(db, user_id)

    existing_item = (
        db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id,
            models.CartItem.product_id == item.product_id).first())

    if existing_item:
        return existing_item

    cart_item = models.CartItem(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity,
        price=item.price)
    
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, user_id: int, item_id: int) -> bool:
    cart = get_create_cart(db, user_id)
    cart_item = (db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id,models.CartItem.id == item_id).first())

    if cart_item is None:
        return False

    db.delete(cart_item)
    db.commit()
    return True


def create_order_from_cart(
    db: Session,
    user_id: int,
    order_in: schemas.OrderCreate) -> models.Order:

    cart = get_create_cart(db, user_id)

    if not cart.cart_items:
        return None

    total_amount: Decimal = Decimal("0.00")
    for item in cart.cart_items:
        total_amount += item.price * item.quantity

    order = models.Order(
        user_id=user_id,
        address=order_in.address,
        total_amount=total_amount)
    
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.cart_items:
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price)
        
        db.add(order_item)

    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(order)

    return order


def get_orders_for_user(db: Session, user_id: int) -> list[models.Order]:
    return (
        db.query(models.Order).filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc()).all()
    )


def get_order(
    db: Session,
    order_id: int,
    user_id: int | None = None) -> models.Order:

    query = db.query(models.Order).filter(models.Order.id == order_id)
    
    if user_id is not None:
        query = query.filter(models.Order.user_id == user_id)

    return query.first()


def update_order(
    db: Session,
    order_id: int,
    status: models.OrderStatus) -> models.Order:
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if order is None:
        return None

    order.status = status
    db.commit()
    return order
