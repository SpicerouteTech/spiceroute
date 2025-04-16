#!/usr/bin/env python3
import sys
import subprocess
import importlib
import os
from typing import List, Tuple
import asyncio
from urllib.parse import urlparse

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python version must be 3.7 or higher")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_package(package: str) -> bool:
    """Check if a package is installed and can be imported"""
    try:
        importlib.import_module(package.split('==')[0])
        return True
    except ImportError:
        return False

def check_required_packages():
    """Check all required packages"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "motor",
        "pymongo",
        "elasticsearch",
        "python-dotenv",
        "pydantic",
        "email-validator",
        "python-jose",
        "python-dateutil",
        "httpx",
        "passlib",
        "python-multipart",
    ]
    
    missing_packages = []
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing packages:", ", ".join(missing_packages))
        print("Run: pip install -e .")
        sys.exit(1)
    print("✅ All required packages are installed")

def check_environment_variables():
    """Check required environment variables"""
    required_vars = [
        "MONGODB_URL",
        "ELASTICSEARCH_URL",
        "JWT_SECRET_KEY",
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "FACEBOOK_CLIENT_ID",
        "FACEBOOK_CLIENT_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:", ", ".join(missing_vars))
        print("Create a .env file with the required variables")
        sys.exit(1)
    print("✅ All required environment variables are set")

async def check_mongodb_connection():
    """Check MongoDB connection"""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        sys.exit(1)

async def check_elasticsearch_connection():
    """Check Elasticsearch connection"""
    try:
        from elasticsearch import AsyncElasticsearch
        es = AsyncElasticsearch([os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")])
        await es.info()
        print("✅ Elasticsearch connection successful")
        await es.close()
    except Exception as e:
        print(f"❌ Elasticsearch connection failed: {str(e)}")
        sys.exit(1)

def create_env_template():
    """Create a template .env file if it doesn't exist"""
    env_template = """# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017/spiceroute

# Elasticsearch Configuration
ELASTICSEARCH_URL=http://localhost:9200

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth2 Configuration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret

# Service Configuration
SERVICE_NAME=auth-service
ENVIRONMENT=development
LOG_LEVEL=INFO
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        print("✅ Created .env template file")
    else:
        print("ℹ️ .env file already exists")

async def main():
    """Main verification function"""
    print("\n🔍 Verifying Auth Service Setup\n")
    
    # Check Python version
    check_python_version()
    
    # Check packages
    check_required_packages()
    
    # Create .env template
    create_env_template()
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception as e:
        print(f"❌ Failed to load .env file: {str(e)}")
        sys.exit(1)
    
    # Check environment variables
    check_environment_variables()
    
    # Check service connections
    await check_mongodb_connection()
    await check_elasticsearch_connection()
    
    print("\n✨ Setup verification completed successfully!")

if __name__ == "__main__":
    asyncio.run(main()) 