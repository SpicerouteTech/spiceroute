import pytest
import requests
import json
from faker import Faker
import os

# Setup test configuration
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"
fake = Faker()

# Mock JWT token for testing (in a real environment, this would be generated from auth service)
TEST_TOKEN = "mock_token_for_testing"


@pytest.fixture
def headers():
    """Headers with mock authorization token."""
    return {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def store_id():
    """Mock store ID for testing."""
    return "6058f12b45783f2b3fc14d23"


@pytest.fixture
def catalog_item_data(store_id):
    """Generate fake catalog item data for testing."""
    return {
        "store_id": store_id,
        "name": fake.unique.word() + " " + fake.word(),
        "description": fake.paragraph(nb_sentences=2),
        "price": round(fake.random_number(2) + fake.random.random(), 2),
        "sale_price": round(fake.random_number(1) + fake.random.random(), 2),
        "unit": fake.random_element(elements=("each", "lb", "kg", "oz", "dozen")),
        "category": [fake.word(), fake.word()],
        "subcategory": fake.word(),
        "image_urls": [fake.image_url()],
        "stock_quantity": fake.random_int(min=1, max=100),
        "is_organic": fake.boolean(),
        "is_vegan": fake.boolean(),
        "is_gluten_free": fake.boolean(),
        "country_of_origin": fake.country(),
        "brand": fake.company(),
        "tags": [fake.word(), fake.word(), fake.word()],
        "featured": fake.boolean(chance_of_getting_true=30)
    }


class TestCatalogService:
    """Test cases for catalog API endpoints."""
    
    item_id = None  # Will store created item ID for use in other tests
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = requests.get(f"{BASE_URL}{API_PREFIX}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_create_item(self, headers, catalog_item_data):
        """Test item creation."""
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/items",
            headers=headers,
            json=catalog_item_data
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == catalog_item_data["name"]
        assert float(data["price"]) == catalog_item_data["price"]
        assert "_id" in data
        
        # Save item ID for other tests
        TestCatalogService.item_id = data["_id"]
    
    def test_get_item(self):
        """Test getting an item by ID."""
        if not TestCatalogService.item_id:
            pytest.skip("Item ID not available - create item test might have failed")
            
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == TestCatalogService.item_id
    
    def test_update_item(self, headers):
        """Test updating an item."""
        if not TestCatalogService.item_id:
            pytest.skip("Item ID not available - create item test might have failed")
            
        # Update the name, price, and stock
        update_data = {
            "name": f"Updated {fake.unique.word()}",
            "price": round(fake.random_number(2) + fake.random.random(), 2),
            "stock_quantity": fake.random_int(min=1, max=100)
        }
        
        response = requests.put(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}",
            headers=headers,
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert float(data["price"]) == update_data["price"]
        assert data["stock_quantity"] == update_data["stock_quantity"]
    
    def test_list_items(self):
        """Test listing items."""
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/items"
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)
    
    def test_search_items(self):
        """Test searching items."""
        if not TestCatalogService.item_id:
            pytest.skip("Item ID not available - create item test might have failed")
            
        # Get the item to extract a search term
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}"
        )
        assert response.status_code == 200
        item_data = response.json()
        
        # Use part of the name as a search term
        search_term = item_data["name"].split()[0]
        
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search?q={search_term}"
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)
        assert len(data["items"]) > 0
    
    def test_get_store_items(self, store_id):
        """Test getting items for a specific store."""
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/stores/{store_id}/items"
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)
        
        # Check all items belong to the specified store
        for item in data["items"]:
            assert item["store_id"] == store_id
    
    def test_update_stock(self, headers):
        """Test updating item stock."""
        if not TestCatalogService.item_id:
            pytest.skip("Item ID not available - create item test might have failed")
            
        # Increase stock by 10
        quantity_change = 10
        
        response = requests.put(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}/stock?quantity_change={quantity_change}",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        
        # Get the current stock to verify the update
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}"
        )
        assert response.status_code == 200
        current_data = response.json()
        
        # Verify stock was increased
        assert current_data["stock_quantity"] == data["stock_quantity"]
    
    def test_delete_item(self, headers):
        """Test deleting an item."""
        if not TestCatalogService.item_id:
            pytest.skip("Item ID not available - create item test might have failed")
            
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}",
            headers=headers
        )
        assert response.status_code == 204
        
        # Verify it's deleted
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/items/{TestCatalogService.item_id}"
        )
        assert response.status_code == 404 