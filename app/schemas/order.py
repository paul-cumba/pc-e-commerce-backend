from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: str
    seller_id: str
    price: float
    freight_value: Optional[float] = 0.0
    shipping_limit_date: Optional[datetime] = None


class OrderItemCreate(OrderItemBase):
    order_item_id: int


class OrderItemInDB(OrderItemBase):
    order_id: str
    order_item_id: int
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_id: str
    order_status: str = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    order_status: Optional[str] = None


class OrderInDBBase(OrderBase):
    order_id: str
    order_purchase_timestamp: datetime
    order_approved_at: Optional[datetime] = None
    order_delivered_carrier_date: Optional[datetime] = None
    order_delivered_customer_date: Optional[datetime] = None
    order_estimated_delivery_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Order(OrderInDBBase):
    items: List[OrderItemInDB] = []
    total_amount: Optional[float] = None


class OrderInDB(OrderInDBBase):
    pass


class OrderResponse(BaseModel):
    order_id: str
    customer_id: str
    order_status: str
    order_purchase_timestamp: datetime
    total_amount: float
    items: List[OrderItemInDB]
    
    class Config:
        from_attributes = True
