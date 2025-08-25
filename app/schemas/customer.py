from pydantic import BaseModel
from typing import Optional


class CustomerBase(BaseModel):
    customer_unique_id: str
    customer_zip_code_prefix: Optional[str] = None
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_zip_code_prefix: Optional[str] = None
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None


class CustomerInDBBase(CustomerBase):
    customer_id: str
    
    class Config:
        from_attributes = True


class Customer(CustomerInDBBase):
    pass


class CustomerInDB(CustomerInDBBase):
    pass
