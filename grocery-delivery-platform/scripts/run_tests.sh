#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Running Tests for Spiceroute Services ---"

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AUTH_SERVICE_DIR="$BASE_DIR/backend/auth-service"
STORE_SERVICE_DIR="$BASE_DIR/backend/store-service"
CATALOG_SERVICE_DIR="$BASE_DIR/backend/catalog-service"

# Install test dependencies if needed
echo "[1/5] Installing test dependencies..."
pip install pytest pytest-cov requests faker

# Function to run tests for a service
run_service_tests() {
    local service_name="$1"
    local service_dir="$2"
    local test_dir="$service_dir/tests"
    
    if [ ! -d "$test_dir" ]; then
        echo "  - No tests found for $service_name at $test_dir"
        return 0
    fi
    
    echo "  - Running tests for $service_name..."
    cd "$service_dir"
    
    # Start the service in the background with test configuration
    echo "    * Starting $service_name service..."
    TEST_MODE=true python src/main.py &
    SERVICE_PID=$!
    
    # Wait for service to start
    echo "    * Waiting for service to start..."
    sleep 5
    
    # Run the tests
    echo "    * Running tests..."
    TEST_BASE_URL="http://localhost:8000" pytest tests/ -v
    
    # Stop the service
    echo "    * Stopping $service_name service..."
    kill $SERVICE_PID
    
    echo "  - Tests completed for $service_name"
}

# Run mock MongoDB for testing
echo "[2/5] Starting mock MongoDB for testing..."
# Use Docker/Podman if available, otherwise skip
if command -v docker &> /dev/null; then
    docker run -d --name test-mongodb -p 27017:27017 mongo:5.0
    MONGODB_CONTAINER="docker"
elif command -v podman &> /dev/null; then
    podman run -d --name test-mongodb -p 27017:27017 mongo:5.0
    MONGODB_CONTAINER="podman"
else
    echo "  - Docker/Podman not found, skipping MongoDB container startup"
    echo "  - Assuming MongoDB is already running on localhost:27017"
    MONGODB_CONTAINER="none"
fi

# Run Auth Service tests
echo "[3/5] Running Auth Service tests..."
run_service_tests "Auth Service" "$AUTH_SERVICE_DIR"

# Run Store Service tests
echo "[4/5] Running Store Service tests..."
run_service_tests "Store Service" "$STORE_SERVICE_DIR"

# Run Catalog Service tests
echo "[5/5] Running Catalog Service tests..."
run_service_tests "Catalog Service" "$CATALOG_SERVICE_DIR"

# Clean up MongoDB container if created
if [ "$MONGODB_CONTAINER" != "none" ]; then
    echo "Cleaning up test MongoDB container..."
    if [ "$MONGODB_CONTAINER" == "docker" ]; then
        docker stop test-mongodb
        docker rm test-mongodb
    else
        podman stop test-mongodb
        podman rm test-mongodb
    fi
fi

echo "--- All tests completed ---" 