from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import product as crud_product
from app.schemas import product as schemas_product

router = APIRouter()


@router.get("/", response_model=List[schemas_product.Product])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get All Products
    
    As a customer, I want to view all available products so I can decide what to purchase.
    Returns a list of all products, including their ID, name, price, and stock availability.
    """
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products


@router.get("/{product_id}", response_model=schemas_product.Product)
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID
    """
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product


@router.post("/", response_model=schemas_product.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas_product.ProductCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new product
    """
    # Check if product already exists
    db_product = crud_product.get_product(db, product_id=product.product_id)
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this ID already exists"
        )
    
    return crud_product.create_product(db=db, product_data=product)


@router.put("/{product_id}", response_model=schemas_product.Product)
def update_product(
    product_id: str,
    product: schemas_product.ProductUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a product
    """
    db_product = crud_product.update_product(db, product_id=product_id, product_data=product)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a product
    """
    success = crud_product.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@router.get("/category/{category}", response_model=List[schemas_product.Product])
def get_products_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get products by category
    """
    products = crud_product.get_products_by_category(db, category=category, skip=skip, limit=limit)
    return products
