import pytest
from fastapi import status


class TestCustomers:
    """Test suite for customer endpoints"""

    def test_register_customer(self, client, sample_customer):
        """Test POST /customers endpoint - Register a New Customer"""
        response = client.post("/api/v1/customers/", json=sample_customer)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "customer_id" in data
        assert data["customer_unique_id"] == sample_customer["customer_unique_id"]
        assert data["customer_city"] == sample_customer["customer_city"]
        assert data["customer_state"] == sample_customer["customer_state"]

    def test_register_duplicate_customer(self, client, sample_customer):
        """Test registering a customer with duplicate unique_id"""
        # Create first customer
        client.post("/api/v1/customers/", json=sample_customer)
        
        # Try to create duplicate
        response = client.post("/api/v1/customers/", json=sample_customer)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_get_all_customers(self, client, sample_customer):
        """Test getting all customers"""
        # Create a customer first
        client.post("/api/v1/customers/", json=sample_customer)
        
        # Get all customers
        response = client.get("/api/v1/customers/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_customer_by_id(self, client, sample_customer):
        """Test getting a specific customer by ID"""
        # Create a customer first
        create_response = client.post("/api/v1/customers/", json=sample_customer)
        customer_id = create_response.json()["customer_id"]
        
        # Get the customer
        response = client.get(f"/api/v1/customers/{customer_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["customer_id"] == customer_id

    def test_get_nonexistent_customer(self, client):
        """Test getting a customer that doesn't exist"""
        response = client.get("/api/v1/customers/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_customer(self, client, sample_customer):
        """Test updating a customer"""
        # Create a customer first
        create_response = client.post("/api/v1/customers/", json=sample_customer)
        customer_id = create_response.json()["customer_id"]
        
        # Update the customer
        update_data = {"customer_city": "Updated City"}
        response = client.put(f"/api/v1/customers/{customer_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["customer_city"] == "Updated City"

    def test_update_nonexistent_customer(self, client):
        """Test updating a customer that doesn't exist"""
        update_data = {"customer_city": "Updated City"}
        response = client.put("/api/v1/customers/nonexistent-id", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_customer(self, client, sample_customer):
        """Test deleting a customer"""
        # Create a customer first
        create_response = client.post("/api/v1/customers/", json=sample_customer)
        customer_id = create_response.json()["customer_id"]
        
        # Delete the customer
        response = client.delete(f"/api/v1/customers/{customer_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = client.get(f"/api/v1/customers/{customer_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_customer(self, client):
        """Test deleting a customer that doesn't exist"""
        response = client.delete("/api/v1/customers/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_customer_orders_empty(self, client, sample_customer):
        """Test GET /customers/{customer_id}/orders with no orders"""
        # Create a customer first
        create_response = client.post("/api/v1/customers/", json=sample_customer)
        customer_id = create_response.json()["customer_id"]
        
        # Get customer orders (should be empty)
        response = client.get(f"/api/v1/customers/{customer_id}/orders")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_customer_orders_nonexistent_customer(self, client):
        """Test getting orders for a customer that doesn't exist"""
        response = client.get("/api/v1/customers/nonexistent-id/orders")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Customer not found" in response.json()["detail"]

    def test_get_customers_by_city(self, client, sample_customer):
        """Test getting customers by city"""
        # Create a customer first
        client.post("/api/v1/customers/", json=sample_customer)
        
        # Get customers by city
        response = client.get(f"/api/v1/customers/city/{sample_customer['customer_city']}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["customer_city"] == sample_customer["customer_city"]

    def test_get_customers_by_state(self, client, sample_customer):
        """Test getting customers by state"""
        # Create a customer first
        client.post("/api/v1/customers/", json=sample_customer)
        
        # Get customers by state
        response = client.get(f"/api/v1/customers/state/{sample_customer['customer_state']}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["customer_state"] == sample_customer["customer_state"]

    def test_customers_pagination(self, client):
        """Test customers pagination"""
        # Create multiple customers
        for i in range(5):
            customer_data = {
                "customer_unique_id": f"test-customer-unique-{i}",
                "customer_city": "Test City",
                "customer_state": "TS"
            }
            client.post("/api/v1/customers/", json=customer_data)
        
        # Test pagination
        response = client.get("/api/v1/customers/?skip=2&limit=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_register_customer_validation(self, client):
        """Test customer registration with invalid data"""
        invalid_customer = {}  # Missing required fields
        response = client.post("/api/v1/customers/", json=invalid_customer)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_customer_minimal_data(self, client):
        """Test customer registration with minimal required data"""
        minimal_customer = {
            "customer_unique_id": "minimal-customer-1"
        }
        response = client.post("/api/v1/customers/", json=minimal_customer)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["customer_unique_id"] == minimal_customer["customer_unique_id"]
        assert data["customer_city"] is None
        assert data["customer_state"] is None
