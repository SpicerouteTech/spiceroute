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
def profile_data():
    """Generate fake profile data for testing."""
    return {
        "user_id": f"test_user_{fake.uuid4()}",
        "store_name": fake.company(),
        "description": fake.catch_phrase(),
        "email": fake.email(),
        "phone": "555-123-4567",
        "category": [fake.word(), fake.word()],
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.zipcode(),
            "country": "USA"
        },
        "business_hours": [
            {
                "day": "Monday",
                "open_time": "09:00",
                "close_time": "18:00",
                "is_closed": False
            }
        ]
    }


class TestStoreProfile:
    """Test cases for store profile API endpoints."""
    
    profile_id = None  # Will store created profile ID for use in other tests
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = requests.get(f"{BASE_URL}{API_PREFIX}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_create_profile(self, headers, profile_data):
        """Test profile creation."""
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/profiles",
            headers=headers,
            json=profile_data
        )
        assert response.status_code == 201
        data = response.json()
        assert data["store_name"] == profile_data["store_name"]
        assert data["email"] == profile_data["email"]
        assert "_id" in data
        
        # Save profile ID for other tests
        TestStoreProfile.profile_id = data["_id"]
    
    def test_get_profile(self, headers):
        """Test getting a profile by ID."""
        if not TestStoreProfile.profile_id:
            pytest.skip("Profile ID not available - create profile test might have failed")
            
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/profiles/{TestStoreProfile.profile_id}",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["_id"] == TestStoreProfile.profile_id
    
    def test_update_profile(self, headers):
        """Test updating a profile."""
        if not TestStoreProfile.profile_id:
            pytest.skip("Profile ID not available - create profile test might have failed")
            
        # Update the store name and description
        update_data = {
            "store_name": f"Updated {fake.company()}",
            "description": fake.catch_phrase()
        }
        
        response = requests.put(
            f"{BASE_URL}{API_PREFIX}/profiles/{TestStoreProfile.profile_id}",
            headers=headers,
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["store_name"] == update_data["store_name"]
        assert data["description"] == update_data["description"]
    
    def test_list_profiles(self, headers):
        """Test listing profiles."""
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/profiles",
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)
    
    def test_delete_profile(self, headers):
        """Test deleting a profile."""
        if not TestStoreProfile.profile_id:
            pytest.skip("Profile ID not available - create profile test might have failed")
            
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/profiles/{TestStoreProfile.profile_id}",
            headers=headers
        )
        assert response.status_code == 204
        
        # Verify it's deleted
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/profiles/{TestStoreProfile.profile_id}",
            headers=headers
        )
        assert response.status_code == 404 