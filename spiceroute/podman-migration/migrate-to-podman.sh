#!/bin/bash

# Script to migrate from Kubernetes to Podman
echo "Starting migration from Kubernetes to Podman..."

# Step 1: Ensure Podman is running
echo "Step 1: Checking Podman status..."

# Check if Lima VM exists
if ! limactl list | grep -q "podman.*Running"; then
    echo "Podman Lima VM is not running. Please start it with:"
    echo "limactl start podman"
    exit 1
fi

# Set Podman socket
export DOCKER_HOST=$(limactl info podman socket)
echo "Using Podman socket: $DOCKER_HOST"

# Step 2: Check if podman-compose is installed
if ! command -v podman-compose &> /dev/null; then
    echo "podman-compose not found. Installing..."
    pip3 install podman-compose
fi

# Step 3: Verify secrets are extracted
if [ ! -f "secrets/mongodb-username.txt" ] || [ ! -f "secrets/mongodb-password.txt" ]; then
    echo "MongoDB secrets files are missing. Extracting from Kubernetes..."
    mkdir -p secrets
    kubectl get secret mongodb-secrets -n spiceroute -o jsonpath='{.data.username}' | base64 -d > secrets/mongodb-username.txt
    kubectl get secret mongodb-secrets -n spiceroute -o jsonpath='{.data.password}' | base64 -d > secrets/mongodb-password.txt
fi

# Step 4: Start Podman containers
echo "Step 4: Starting Podman containers..."
podman-compose up -d

echo "Step 5: Verifying container status..."
podman-compose ps

# Step A: Fetch data and import into Podman MongoDB
echo "Do you want to export data from Kubernetes MongoDB and import to Podman? (y/n)"
read -r export_data

if [[ "$export_data" =~ ^[Yy]$ ]]; then
    echo "Exporting data from Kubernetes MongoDB..."
    
    # Create tmp directory
    mkdir -p tmp_data
    
    # Export data from Kubernetes MongoDB
    echo "Creating MongoDB dump from Kubernetes pod..."
    K8S_MONGO_POD=$(kubectl get pods -n spiceroute -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
    kubectl exec -n spiceroute $K8S_MONGO_POD -- mongodump --out=/tmp/mongodump
    
    # Copy dump to local
    echo "Copying dump to local machine..."
    kubectl cp spiceroute/$K8S_MONGO_POD:/tmp/mongodump tmp_data/mongodump
    
    # Import to Podman MongoDB
    echo "Importing data to Podman MongoDB..."
    PODMAN_MONGO_CONTAINER=$(podman ps --filter name=spiceroute-mongodb -q)
    podman cp tmp_data/mongodump $PODMAN_MONGO_CONTAINER:/tmp/
    podman exec $PODMAN_MONGO_CONTAINER mongorestore --username $(cat secrets/mongodb-username.txt) --password $(cat secrets/mongodb-password.txt) --authenticationDatabase admin /tmp/mongodump
    
    # Clean up
    rm -rf tmp_data
    echo "Data migration completed!"
fi

# Step 6: Optional - Clean up Kubernetes resources
echo "Do you want to clean up Kubernetes resources? (y/n)"
read -r cleanup

if [[ "$cleanup" =~ ^[Yy]$ ]]; then
    echo "Cleaning up Kubernetes resources..."
    kubectl delete -n spiceroute deployment/mongodb deployment/elasticsearch
    kubectl delete -n spiceroute service/mongodb service/elasticsearch
    kubectl delete -n spiceroute pvc/mongodb-pvc pvc/elasticsearch-pvc
    kubectl delete -n spiceroute secret/mongodb-secrets
    echo "Kubernetes resources deleted!"
else
    echo "Keeping Kubernetes resources for now."
fi

echo "
Migration to Podman completed! Your services are now running in Podman:
- MongoDB: localhost:27017
- Elasticsearch: localhost:9200

You can manage them using:
- podman-compose ps
- podman-compose logs
- podman-compose down (to stop)

For a GUI interface, use Podman Desktop.
" 