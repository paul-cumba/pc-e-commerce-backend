import pytest
from fastapi import status


class TestOrders:
    """Test suite for order endpoints"""

    def setup_test_data(self, client):
        """Helper method to set up test data"""
        # Create a customer
        customer_data = {
            "customer_unique_id": "test-customer-unique-1",
            "customer_city": "Test City",
            "customer_state": "TS"
        }
        customer_response = client.post("/api/v1/customers/", json=customer_data)
        customer_id = customer_response.json()["customer_id"]
        
        # Create a product
        product_data = {
            "product_id": "test-product-1",
            "product_category_name": "electronics",
            "product_name_length": 50
        }
        client.post("/api/v1/products/", json=product_data)
        
        return customer_id

    def test_create_order(self, client):
        """Test POST /orders endpoint - Create an Order"""
        customer_id = self.setup_test_data(client)
        
        order_data = {
            "customer_id": customer_id,
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
        
        response = client.post("/api/v1/orders/", json=order_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "order_id" in data
        assert data["customer_id"] == customer_id
        assert data["order_status"] == "pending"
        assert data["total_amount"] == 109.99  # price + freight_value
        assert len(data["items"]) == 1

    def test_create_order_nonexistent_customer(self, client):
        """Test creating an order with nonexistent customer"""
        order_data = {
            "customer_id": "nonexistent-customer",
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
        
        response = client.post("/api/v1/orders/", json=order_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Customer not found" in response.json()["detail"]

    def test_create_order_nonexistent_product(self, client):
        """Test creating an order with nonexistent product"""
        customer_id = self.setup_test_data(client)
        
        order_data = {
            "customer_id": customer_id,
            "order_status": "pending",
            "items": [
                {
                    "order_item_id": 1,
                    "product_id": "nonexistent-product",
                    "seller_id": "test-seller-1",
                    "price": 99.99,
                    "freight_value": 10.0
                }
            ]
        }
        
        response = client.post("/api/v1/orders/", json=order_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Product nonexistent-product not found" in response.json()["detail"]

    def test_get_all_orders(self, client):
        """Test getting all orders"""
        customer_id = self.setup_test_data(client)
        
        # Create an order first
        order_data = {
            "customer_id": customer_id,
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
        client.post("/api/v1/orders/", json=order_data)
        
        # Get all orders
        response = client.get("/api/v1/orders/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_order_by_id(self, client):
        """Test getting a specific order by ID"""
        customer_id = self.setup_test_data(client)
        
        # Create an order first
        order_data = {
            "customer_id": customer_id,
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
        create_response = client.post("/api/v1/orders/", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Get the order
        response = client.get(f"/api/v1/orders/{order_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["order_id"] == order_id

    def test_get_nonexistent_order(self, client):
        """Test getting an order that doesn't exist"""
        response = client.get("/api/v1/orders/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Order not found" in response.json()["detail"]

    def test_update_order(self, client):
        """Test updating an order"""
        customer_id = self.setup_test_data(client)
        
        # Create an order first
        order_data = {
            "customer_id": customer_id,
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
        create_response = client.post("/api/v1/orders/", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Update the order
        update_data = {"order_status": "confirmed"}
        response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["order_status"] == "confirmed"

    def test_update_nonexistent_order(self, client):
        """Test updating an order that doesn't exist"""
        update_data = {"order_status": "confirmed"}
        response = client.put("/api/v1/orders/nonexistent-id", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_order(self, client):
        """Test deleting an order"""
        customer_id = self.setup_test_data(client)
        
        # Create an order first
        order_data = {
            "customer_id": customer_id,
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
        create_response = client.post("/api/v1/orders/", json=order_data)
        order_id = create_response.json()["order_id"]
        
        # Delete the order
        response = client.delete(f"/api/v1/orders/{order_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = client.get(f"/api/v1/orders/{order_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_order(self, client):
        """Test deleting an order that doesn't exist"""
        response = client.delete("/api/v1/orders/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_orders_by_status(self, client):
        """Test getting orders by status"""
        customer_id = self.setup_test_data(client)
        
        # Create orders with different statuses
        order_data_1 = {
            "customer_id": customer_id,
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
        order_data_2 = {
            "customer_id": customer_id,
            "order_status": "confirmed",
            "items": [
                {
                    "order_item_id": 1,
                    "product_id": "test-product-1",
                    "seller_id": "test-seller-1",
                    "price": 149.99,
                    "freight_value": 15.0
                }
            ]
        }
        
        client.post("/api/v1/orders/", json=order_data_1)
        client.post("/api/v1/orders/", json=order_data_2)
        
        # Get orders by status
        response = client.get("/api/v1/orders/status/pending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(order["order_status"] == "pending" for order in data)

    def test_get_customer_orders_with_orders(self, client):
        """Test GET /customers/{customer_id}/orders with existing orders"""
        customer_id = self.setup_test_data(client)
        
        # Create an order
        order_data = {
            "customer_id": customer_id,
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
        client.post("/api/v1/orders/", json=order_data)
        
        # Get customer orders
        response = client.get(f"/api/v1/customers/{customer_id}/orders")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["customer_id"] == customer_id
        assert "total_amount" in data[0]
        assert "items" in data[0]

    def test_create_order_multiple_items(self, client):
        """Test creating an order with multiple items"""
        customer_id = self.setup_test_data(client)
        
        # Create another product
        product_data_2 = {
            "product_id": "test-product-2",
            "product_category_name": "books",
            "product_name_length": 30
        }
        client.post("/api/v1/products/", json=product_data_2)
        
        order_data = {
            "customer_id": customer_id,
            "order_status": "pending",
            "items": [
                {
                    "order_item_id": 1,
                    "product_id": "test-product-1",
                    "seller_id": "test-seller-1",
                    "price": 99.99,
                    "freight_value": 10.0
                },
                {
                    "order_item_id": 2,
                    "product_id": "test-product-2",
                    "seller_id": "test-seller-2",
                    "price": 29.99,
                    "freight_value": 5.0
                }
            ]
        }
        
        response = client.post("/api/v1/orders/", json=order_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total_amount"] == 144.98  # (99.99 + 10.0) + (29.99 + 5.0)

    def test_create_order_validation(self, client):
        """Test order creation with invalid data"""
        invalid_order = {}  # Missing required fields
        response = client.post("/api/v1/orders/", json=invalid_order)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_orders_pagination(self, client):
        """Test orders pagination"""
        customer_id = self.setup_test_data(client)
        
        # Create multiple orders
        for i in range(5):
            order_data = {
                "customer_id": customer_id,
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
            client.post("/api/v1/orders/", json=order_data)
        
        # Test pagination
        response = client.get("/api/v1/orders/?skip=2&limit=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
