import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from ..models import StoreOwnerCreate, StoreOwnerStatus, OAuthProvider
from ..db import store_owner_db
from ..router import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_store_owner():
    # Test creating a store owner
    store_owner = StoreOwnerCreate(
        email="test@example.com",
        full_name="Test User",
        oauth_provider=OAuthProvider.GOOGLE,
        oauth_id="123456789",
        status=StoreOwnerStatus.ACTIVE
    )
    
    created_owner = await store_owner_db.create_store_owner(store_owner)
    assert created_owner.email == store_owner.email
    assert created_owner.full_name == store_owner.full_name
    assert created_owner.oauth_provider == store_owner.oauth_provider

@pytest.mark.asyncio
async def test_get_store_owner():
    # Test retrieving a store owner
    owner = await store_owner_db.get_store_owner_by_email("test@example.com")
    assert owner is not None
    assert owner.email == "test@example.com"

@pytest.mark.asyncio
async def test_create_invite():
    # Test creating an invitation
    invite = await store_owner_db.create_invite(
        email="newuser@example.com",
        invited_by="test@example.com"
    )
    assert invite.email == "newuser@example.com"
    assert invite.invited_by == "test@example.com"
    assert not invite.is_used

@pytest.mark.asyncio
async def test_verify_invite():
    # Test verifying an invitation
    invite = await store_owner_db.get_invite_by_token("test_token")
    if invite:
        assert invite.email == "newuser@example.com"
        assert not invite.is_used

def test_google_login_url():
    # Test Google login URL generation
    response = client.get("/auth/store-owner/google/login")
    assert response.status_code == 200
    assert "url" in response.json()

def test_facebook_login_url():
    # Test Facebook login URL generation
    response = client.get("/auth/store-owner/facebook/login")
    assert response.status_code == 200
    assert "url" in response.json()

@pytest.mark.asyncio
async def test_invite_store_owner():
    # Test store owner invitation endpoint
    response = client.post(
        "/auth/store-owner/invite",
        json={"email": "newuser@example.com"}
    )
    assert response.status_code == 401  # Should fail without authentication

def test_verify_invite_endpoint():
    # Test invite verification endpoint
    response = client.get("/auth/store-owner/verify-invite/test_token")
    assert response.status_code == 200 