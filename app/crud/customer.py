from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import customer
import uuid


def get_customer(db: Session, customer_id: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.customer_id == customer_id).first()


def get_customer_by_unique_id(db: Session, unique_id: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.customer_unique_id == unique_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer_data: customer.CustomerCreate) -> models.Customer:
    # Generate a unique customer_id
    customer_id = str(uuid.uuid4())
    
    db_customer = models.Customer(
        customer_id=customer_id,
        **customer_data.dict()
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(
    db: Session, customer_id: str, customer_data: customer.CustomerUpdate
) -> Optional[models.Customer]:
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: str) -> bool:
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return True
    return False


def get_customers_by_city(
    db: Session, city: str, skip: int = 0, limit: int = 100
) -> List[models.Customer]:
    return (
        db.query(models.Customer)
        .filter(models.Customer.customer_city == city)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_customers_by_state(
    db: Session, state: str, skip: int = 0, limit: int = 100
) -> List[models.Customer]:
    return (
        db.query(models.Customer)
        .filter(models.Customer.customer_state == state)
        .offset(skip)
        .limit(limit)
        .all()
    )
