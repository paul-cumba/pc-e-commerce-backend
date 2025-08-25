from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(String, primary_key=True, index=True)
    product_category_name = Column(String, index=True)
    product_name_length = Column(Integer)
    product_description_length = Column(Integer)
    product_photos_qty = Column(Integer)
    product_weight_g = Column(Float)
    product_length_cm = Column(Float)
    product_height_cm = Column(Float)
    product_width_cm = Column(Float)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String, primary_key=True, index=True)
    customer_unique_id = Column(String, unique=True, index=True)
    customer_zip_code_prefix = Column(String)
    customer_city = Column(String)
    customer_state = Column(String)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")


class Seller(Base):
    __tablename__ = "sellers"
    
    seller_id = Column(String, primary_key=True, index=True)
    seller_zip_code_prefix = Column(String)
    seller_city = Column(String)
    seller_state = Column(String)
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="seller")


class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    order_status = Column(String)
    order_purchase_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    order_approved_at = Column(DateTime(timezone=True))
    order_delivered_carrier_date = Column(DateTime(timezone=True))
    order_delivered_customer_date = Column(DateTime(timezone=True))
    order_estimated_delivery_date = Column(DateTime(timezone=True))
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")
    order_payments = relationship("OrderPayment", back_populates="order")
    order_reviews = relationship("OrderReview", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True)
    order_item_id = Column(Integer, primary_key=True)
    product_id = Column(String, ForeignKey("products.product_id"))
    seller_id = Column(String, ForeignKey("sellers.seller_id"))
    shipping_limit_date = Column(DateTime(timezone=True))
    price = Column(Float)
    freight_value = Column(Float)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    seller = relationship("Seller", back_populates="order_items")


class OrderPayment(Base):
    __tablename__ = "order_payments"
    
    order_id = Column(String, ForeignKey("orders.order_id"), primary_key=True)
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String)
    payment_installments = Column(Integer)
    payment_value = Column(Float)
    
    # Relationships
    order = relationship("Order", back_populates="order_payments")


class OrderReview(Base):
    __tablename__ = "order_reviews"
    
    review_id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.order_id"))
    review_score = Column(Integer)
    review_comment_title = Column(String)
    review_comment_message = Column(Text)
    review_creation_date = Column(DateTime(timezone=True))
    review_answer_timestamp = Column(DateTime(timezone=True))
    
    # Relationships
    order = relationship("Order", back_populates="order_reviews")


class Geolocation(Base):
    __tablename__ = "geolocation"
    
    geolocation_zip_code_prefix = Column(String, primary_key=True)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)


class ProductCategoryNameTranslation(Base):
    __tablename__ = "product_category_name_translation"
    
    product_category_name = Column(String, primary_key=True)
    product_category_name_english = Column(String)


class LeadsQualified(Base):
    __tablename__ = "leads_qualified"
    
    mql_id = Column(String, primary_key=True, index=True)
    first_contact_date = Column(DateTime(timezone=True))
    landing_page_id = Column(String)
    origin = Column(String)


class LeadsClosed(Base):
    __tablename__ = "leads_closed"
    
    mql_id = Column(String, primary_key=True, index=True)
    seller_id = Column(String)
    sdr_id = Column(String)
    sr_id = Column(String)
    won_date = Column(DateTime(timezone=True))
    business_segment = Column(String)
    lead_type = Column(String)
    lead_behaviour_profile = Column(String)
    has_gtin = Column(Boolean)
    average_stock = Column(String)
    business_type = Column(String)
    declared_product_catalog_size = Column(Float)
    declared_monthly_revenue = Column(Float)
