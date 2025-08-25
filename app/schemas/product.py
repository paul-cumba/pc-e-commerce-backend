from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    product_category_name: Optional[str] = None
    product_name_length: Optional[int] = None
    product_description_length: Optional[int] = None
    product_photos_qty: Optional[int] = None
    product_weight_g: Optional[float] = None
    product_length_cm: Optional[float] = None
    product_height_cm: Optional[float] = None
    product_width_cm: Optional[float] = None


class ProductCreate(ProductBase):
    product_id: str


class ProductUpdate(ProductBase):
    pass


class ProductInDBBase(ProductBase):
    product_id: str
    
    class Config:
        from_attributes = True


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass
