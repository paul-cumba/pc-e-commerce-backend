import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_product():
    return {
        "product_id": "test-product-1",
        "product_category_name": "electronics",
        "product_name_length": 50,
        "product_description_length": 200,
        "product_photos_qty": 3,
        "product_weight_g": 500.0,
        "product_length_cm": 20.0,
        "product_height_cm": 15.0,
        "product_width_cm": 10.0
    }


@pytest.fixture
def sample_customer():
    return {
        "customer_unique_id": "test-customer-unique-1",
        "customer_zip_code_prefix": "12345",
        "customer_city": "Test City",
        "customer_state": "TS"
    }


@pytest.fixture
def sample_order():
    return {
        "customer_id": "test-customer-1",
        "order_status": "pending",
        "items": [
            {
                "order_item_id": 1,
                "product_id": "test-product-1",
                "seller_id": "test-seller-1",
                "price": 99.99,
                "freight_value": 10.0
            }
        ]
    }
