# E-commerce Backend API

A comprehensive REST API for an E-commerce application built with Python, FastAPI, and SQLAlchemy. This API serves as the backend for managing products, customers, orders, and related data.

## Features

- **Product Management**: Create, read, update, and delete products
- **Customer Management**: Register customers and manage their information
- **Order Management**: Create orders, track order history, and manage order status
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Comprehensive Testing**: Full test suite with pytest
- **Input Validation**: Pydantic models for request/response validation
- **Error Handling**: Proper HTTP status codes and error messages

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: pytest
- **Documentation**: OpenAPI/Swagger (auto-generated)

## API Endpoints

### Products
- `GET /api/v1/products/` - Get all products
- `GET /api/v1/products/{product_id}` - Get product by ID
- `POST /api/v1/products/` - Create new product
- `PUT /api/v1/products/{product_id}` - Update product
- `DELETE /api/v1/products/{product_id}` - Delete product
- `GET /api/v1/products/category/{category}` - Get products by category

### Customers
- `POST /api/v1/customers/` - Register new customer
- `GET /api/v1/customers/` - Get all customers
- `GET /api/v1/customers/{customer_id}` - Get customer by ID
- `PUT /api/v1/customers/{customer_id}` - Update customer
- `DELETE /api/v1/customers/{customer_id}` - Delete customer
- `GET /api/v1/customers/{customer_id}/orders` - Get customer's orders
- `GET /api/v1/customers/city/{city}` - Get customers by city
- `GET /api/v1/customers/state/{state}` - Get customers by state

### Orders
- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/` - Get all orders
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `PUT /api/v1/orders/{order_id}` - Update order
- `DELETE /api/v1/orders/{order_id}` - Delete order
- `GET /api/v1/orders/status/{status}` - Get orders by status

## User Stories Implementation

### 1. Get All Products
**Endpoint**: `GET /api/v1/products/`
**Description**: As a customer, I want to view all available products so I can decide what to purchase.
**Output**: List of all products with ID, name, category, and specifications.

### 2. Register a New Customer
**Endpoint**: `POST /api/v1/customers/`
**Description**: As a new user, I want to register so I can make purchases.
**Input**: Customer details (unique ID, zip code, city, state)
**Output**: Created customer information with system-generated customer ID.

### 3. Create an Order
**Endpoint**: `POST /api/v1/orders/`
**Description**: As a customer, I want to place an order so I can purchase items.
**Input**: Customer ID, list of product items with quantities and prices, order status
**Output**: Order confirmation with order ID, total amount, and success status.

### 4. View Customer's Orders
**Endpoint**: `GET /api/v1/customers/{customer_id}/orders`
**Description**: As a customer, I want to view my order history so I can track my purchases.
**Output**: List of customer's orders with order ID, status, timestamp, total amount, and items.

## Installation and Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### 1. Clone the repository
```bash
git clone https://github.com/paul-cumba/pc-e-commerce-backend.git
cd pc-e-commerce-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your database credentials and configuration
```

### 5. Set up the database

#### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL with Docker Compose
docker-compose up -d postgres

# Initialize database tables
python -m app.db.init_db

# Or use the automated setup script:
# On macOS/Linux:
./scripts/setup-docker.sh

# On Windows:
scripts\setup-docker.bat
```

#### Option B: Local PostgreSQL Installation
```bash
# Create PostgreSQL database
createdb ecommerce_db

# Initialize database tables
python -m app.db.init_db
```

### 6. Run the application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 7. Access API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app
```

Run specific test files:
```bash
pytest tests/test_products.py
pytest tests/test_customers.py
pytest tests/test_orders.py
```

## Project Structure

```
pc-e-commerce-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configuration settings
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py        # Database connection
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py         # Product Pydantic schemas
│   │   ├── customer.py        # Customer Pydantic schemas
│   │   └── order.py           # Order Pydantic schemas
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── product.py         # Product CRUD operations
│   │   ├── customer.py        # Customer CRUD operations
│   │   └── order.py           # Order CRUD operations
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── api.py         # API router
│           └── endpoints/
│               ├── __init__.py
│               ├── products.py    # Product endpoints
│               ├── customers.py   # Customer endpoints
│               └── orders.py      # Order endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Test configuration
│   ├── test_products.py       # Product endpoint tests
│   ├── test_customers.py      # Customer endpoint tests
│   └── test_orders.py         # Order endpoint tests
├── requirements.txt           # Python dependencies
├── pytest.ini               # Pytest configuration
├── .env.example             # Environment variables example
└── README.md               # This file
```

## Database Schema

The application uses the following main entities based on the provided database schema:

- **Products**: Product information including category, dimensions, weight
- **Customers**: Customer details including location information
- **Orders**: Order information with timestamps and status
- **Order Items**: Individual items within orders with pricing
- **Order Payments**: Payment information for orders
- **Order Reviews**: Customer reviews for orders
- **Sellers**: Seller information
- **Geolocation**: Location data for zip codes

## API Response Examples

### Get All Products
```json
[
  {
    "product_id": "prod-123",
    "product_category_name": "electronics",
    "product_name_length": 50,
    "product_description_length": 200,
    "product_photos_qty": 3,
    "product_weight_g": 500.0,
    "product_length_cm": 20.0,
    "product_height_cm": 15.0,
    "product_width_cm": 10.0
  }
]
```

### Register Customer
```json
{
  "customer_id": "cust-456",
  "customer_unique_id": "unique-789",
  "customer_zip_code_prefix": "12345",
  "customer_city": "New York",
  "customer_state": "NY"
}
```

### Create Order Response
```json
{
  "order_id": "order-789",
  "customer_id": "cust-456",
  "order_status": "pending",
  "order_purchase_timestamp": "2024-01-15T10:30:00Z",
  "total_amount": 109.99,
  "items": [
    {
      "order_id": "order-789",
      "order_item_id": 1,
      "product_id": "prod-123",
      "seller_id": "seller-001",
      "price": 99.99,
      "freight_value": 10.0,
      "shipping_limit_date": null
    }
  ]
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET requests
- `201 Created` - Successful POST requests
- `204 No Content` - Successful DELETE requests
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.
