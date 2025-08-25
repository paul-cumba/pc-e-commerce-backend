import pytest
from fastapi import status


class TestProducts:
    """Test suite for product endpoints"""

    def test_create_product(self, client, sample_product):
        """Test creating a new product"""
        response = client.post("/api/v1/products/", json=sample_product)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["product_id"] == sample_product["product_id"]
        assert data["product_category_name"] == sample_product["product_category_name"]

    def test_create_duplicate_product(self, client, sample_product):
        """Test creating a product with duplicate ID"""
        # Create first product
        client.post("/api/v1/products/", json=sample_product)
        
        # Try to create duplicate
        response = client.post("/api/v1/products/", json=sample_product)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_get_all_products(self, client, sample_product):
        """Test GET /products endpoint"""
        # Create a product first
        client.post("/api/v1/products/", json=sample_product)
        
        # Get all products
        response = client.get("/api/v1/products/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["product_id"] == sample_product["product_id"]

    def test_get_product_by_id(self, client, sample_product):
        """Test getting a specific product by ID"""
        # Create a product first
        client.post("/api/v1/products/", json=sample_product)
        
        # Get the product
        response = client.get(f"/api/v1/products/{sample_product['product_id']}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_id"] == sample_product["product_id"]

    def test_get_nonexistent_product(self, client):
        """Test getting a product that doesn't exist"""
        response = client.get("/api/v1/products/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_update_product(self, client, sample_product):
        """Test updating a product"""
        # Create a product first
        client.post("/api/v1/products/", json=sample_product)
        
        # Update the product
        update_data = {"product_category_name": "updated_category"}
        response = client.put(f"/api/v1/products/{sample_product['product_id']}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_category_name"] == "updated_category"

    def test_update_nonexistent_product(self, client):
        """Test updating a product that doesn't exist"""
        update_data = {"product_category_name": "updated_category"}
        response = client.put("/api/v1/products/nonexistent-id", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product(self, client, sample_product):
        """Test deleting a product"""
        # Create a product first
        client.post("/api/v1/products/", json=sample_product)
        
        # Delete the product
        response = client.delete(f"/api/v1/products/{sample_product['product_id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify it's deleted
        response = client.get(f"/api/v1/products/{sample_product['product_id']}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_product(self, client):
        """Test deleting a product that doesn't exist"""
        response = client.delete("/api/v1/products/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_products_by_category(self, client, sample_product):
        """Test getting products by category"""
        # Create a product first
        client.post("/api/v1/products/", json=sample_product)
        
        # Get products by category
        response = client.get(f"/api/v1/products/category/{sample_product['product_category_name']}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["product_category_name"] == sample_product["product_category_name"]

    def test_get_products_pagination(self, client):
        """Test products pagination"""
        # Create multiple products
        for i in range(5):
            product_data = {
                "product_id": f"test-product-{i}",
                "product_category_name": "electronics"
            }
            client.post("/api/v1/products/", json=product_data)
        
        # Test pagination
        response = client.get("/api/v1/products/?skip=2&limit=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_create_product_validation(self, client):
        """Test product creation with invalid data"""
        invalid_product = {}  # Missing required fields
        response = client.post("/api/v1/products/", json=invalid_product)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
