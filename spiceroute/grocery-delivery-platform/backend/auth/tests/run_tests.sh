#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run MongoDB in the background if not already running
if ! mongosh --eval "db.version()" > /dev/null 2>&1; then
    echo "Starting MongoDB..."
    mongod --dbpath ./data/db --fork --logpath ./data/mongodb.log
fi

# Run the tests
pytest -v tests/test_auth.py

# Clean up
if [ -f "./data/mongodb.log" ]; then
    echo "Cleaning up MongoDB..."
    mongod --shutdown
    rm -rf ./data
fi 