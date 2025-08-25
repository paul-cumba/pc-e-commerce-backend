from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import order as crud_order
from app.crud import customer as crud_customer
from app.crud import product as crud_product
from app.schemas import order as schemas_order

router = APIRouter()


@router.post("/", response_model=schemas_order.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: schemas_order.OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create an Order
    
    As a customer, I want to place an order so I can purchase items.
    Expected Input: The customer ID, a list of product items (including their ID, quantity, and price), 
    and the order status.
    Expected Output: Order confirmation with the order ID, total amount, and success status.
    """
    # Validate customer exists
    db_customer = crud_customer.get_customer(db, customer_id=order.customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Validate all products exist
    for item in order.items:
        db_product = crud_product.get_product(db, product_id=item.product_id)
        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.product_id} not found"
            )
    
    # Create the order
    db_order = crud_order.create_order(db=db, order_data=order)
    
    # Calculate total amount
    total_amount = crud_order.get_order_total(db, db_order.order_id)
    
    # Return order response
    return schemas_order.OrderResponse(
        order_id=db_order.order_id,
        customer_id=db_order.customer_id,
        order_status=db_order.order_status,
        order_purchase_timestamp=db_order.order_purchase_timestamp,
        total_amount=total_amount,
        items=db_order.order_items
    )


@router.get("/", response_model=List[schemas_order.OrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all orders
    """
    orders = crud_order.get_orders(db, skip=skip, limit=limit)
    
    order_responses = []
    for order in orders:
        total_amount = crud_order.get_order_total(db, order.order_id)
        order_response = schemas_order.OrderResponse(
            order_id=order.order_id,
            customer_id=order.customer_id,
            order_status=order.order_status,
            order_purchase_timestamp=order.order_purchase_timestamp,
            total_amount=total_amount,
            items=order.order_items
        )
        order_responses.append(order_response)
    
    return order_responses


@router.get("/{order_id}", response_model=schemas_order.OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific order by ID
    """
    db_order = crud_order.get_order_with_items(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    total_amount = crud_order.get_order_total(db, order_id)
    
    return schemas_order.OrderResponse(
        order_id=db_order.order_id,
        customer_id=db_order.customer_id,
        order_status=db_order.order_status,
        order_purchase_timestamp=db_order.order_purchase_timestamp,
        total_amount=total_amount,
        items=db_order.order_items
    )


@router.put("/{order_id}", response_model=schemas_order.OrderResponse)
def update_order(
    order_id: str,
    order: schemas_order.OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an order (typically status changes)
    """
    db_order = crud_order.update_order(db, order_id=order_id, order_data=order)
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    total_amount = crud_order.get_order_total(db, order_id)
    
    return schemas_order.OrderResponse(
        order_id=db_order.order_id,
        customer_id=db_order.customer_id,
        order_status=db_order.order_status,
        order_purchase_timestamp=db_order.order_purchase_timestamp,
        total_amount=total_amount,
        items=db_order.order_items
    )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an order
    """
    success = crud_order.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )


@router.get("/status/{status}", response_model=List[schemas_order.OrderResponse])
def get_orders_by_status(
    status: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get orders by status
    """
    orders = crud_order.get_orders_by_status(db, status=status, skip=skip, limit=limit)
    
    order_responses = []
    for order in orders:
        total_amount = crud_order.get_order_total(db, order.order_id)
        order_response = schemas_order.OrderResponse(
            order_id=order.order_id,
            customer_id=order.customer_id,
            order_status=order.order_status,
            order_purchase_timestamp=order.order_purchase_timestamp,
            total_amount=total_amount,
            items=order.order_items
        )
        order_responses.append(order_response)
    
    return order_responses
