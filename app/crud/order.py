from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import models
from app.schemas import order
import uuid


def get_order(db: Session, order_id: str) -> Optional[models.Order]:
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_customer_orders(
    db: Session, customer_id: str, skip: int = 0, limit: int = 100
) -> List[models.Order]:
    return (
        db.query(models.Order)
        .filter(models.Order.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_order(db: Session, order_data: order.OrderCreate) -> models.Order:
    # Generate a unique order_id
    order_id = str(uuid.uuid4())
    
    # Create the order
    db_order = models.Order(
        order_id=order_id,
        customer_id=order_data.customer_id,
        order_status=order_data.order_status
    )
    db.add(db_order)
    db.flush()  # Flush to get the order_id for order items
    
    # Create order items
    for item_data in order_data.items:
        db_order_item = models.OrderItem(
            order_id=order_id,
            order_item_id=item_data.order_item_id,
            product_id=item_data.product_id,
            seller_id=item_data.seller_id,
            price=item_data.price,
            freight_value=item_data.freight_value,
            shipping_limit_date=item_data.shipping_limit_date
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(
    db: Session, order_id: str, order_data: order.OrderUpdate
) -> Optional[models.Order]:
    db_order = get_order(db, order_id)
    if db_order:
        update_data = order_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: str) -> bool:
    db_order = get_order(db, order_id)
    if db_order:
        # Delete order items first
        db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
        # Delete order payments
        db.query(models.OrderPayment).filter(models.OrderPayment.order_id == order_id).delete()
        # Delete order reviews
        db.query(models.OrderReview).filter(models.OrderReview.order_id == order_id).delete()
        # Delete the order
        db.delete(db_order)
        db.commit()
        return True
    return False


def get_order_with_items(db: Session, order_id: str) -> Optional[models.Order]:
    return (
        db.query(models.Order)
        .filter(models.Order.order_id == order_id)
        .first()
    )


def get_order_total(db: Session, order_id: str) -> float:
    total = (
        db.query(func.sum(models.OrderItem.price + models.OrderItem.freight_value))
        .filter(models.OrderItem.order_id == order_id)
        .scalar()
    )
    return total or 0.0


def get_orders_by_status(
    db: Session, status: str, skip: int = 0, limit: int = 100
) -> List[models.Order]:
    return (
        db.query(models.Order)
        .filter(models.Order.order_status == status)
        .offset(skip)
        .limit(limit)
        .all()
    )
