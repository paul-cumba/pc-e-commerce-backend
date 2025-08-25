from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import models
from app.schemas import product


def get_product(db: Session, product_id: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.product_id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product_data: product.ProductCreate) -> models.Product:
    db_product = models.Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, product_id: str, product_data: product.ProductUpdate
) -> Optional[models.Product]:
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: str) -> bool:
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def get_products_by_category(
    db: Session, category: str, skip: int = 0, limit: int = 100
) -> List[models.Product]:
    return (
        db.query(models.Product)
        .filter(models.Product.product_category_name == category)
        .offset(skip)
        .limit(limit)
        .all()
    )
