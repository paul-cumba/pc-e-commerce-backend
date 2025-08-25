from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import customer as crud_customer
from app.crud import order as crud_order
from app.schemas import customer as schemas_customer
from app.schemas import order as schemas_order

router = APIRouter()


@router.post("/", response_model=schemas_customer.Customer, status_code=status.HTTP_201_CREATED)
def register_customer(
    customer: schemas_customer.CustomerCreate,
    db: Session = Depends(get_db)
):
    """
    Register a New Customer
    
    As a new user, I want to register so I can make purchases.
    Expected Input: Customer details like unique ID, zip code, city, and state.
    Expected Output: The created customer's information, including their system-generated customer ID.
    """
    # Check if customer with unique_id already exists
    db_customer = crud_customer.get_customer_by_unique_id(db, unique_id=customer.customer_unique_id)
    if db_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this unique ID already exists"
        )
    
    return crud_customer.create_customer(db=db, customer_data=customer)


@router.get("/", response_model=List[schemas_customer.Customer])
def get_all_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all customers
    """
    customers = crud_customer.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=schemas_customer.Customer)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific customer by ID
    """
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer


@router.get("/{customer_id}/orders", response_model=List[schemas_order.OrderResponse])
def get_customer_orders(
    customer_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    View Customer's Orders
    
    As a customer, I want to view my order history so I can track my purchases.
    Expected Output: A list of all the customer's orders, including details like order ID, 
    status, purchase timestamp, total amount, and items purchased.
    """
    # First check if customer exists
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get customer orders
    orders = crud_order.get_customer_orders(db, customer_id=customer_id, skip=skip, limit=limit)
    
    # Build response with order totals and items
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


@router.put("/{customer_id}", response_model=schemas_customer.Customer)
def update_customer(
    customer_id: str,
    customer: schemas_customer.CustomerUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a customer
    """
    db_customer = crud_customer.update_customer(db, customer_id=customer_id, customer_data=customer)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return db_customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a customer
    """
    success = crud_customer.delete_customer(db, customer_id=customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )


@router.get("/city/{city}", response_model=List[schemas_customer.Customer])
def get_customers_by_city(
    city: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get customers by city
    """
    customers = crud_customer.get_customers_by_city(db, city=city, skip=skip, limit=limit)
    return customers


@router.get("/state/{state}", response_model=List[schemas_customer.Customer])
def get_customers_by_state(
    state: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get customers by state
    """
    customers = crud_customer.get_customers_by_state(db, state=state, skip=skip, limit=limit)
    return customers
