#!/bin/bash

# Start Minikube with Podman driver
echo "Starting Minikube with Podman driver..."
minikube start --driver=podman

# Create namespace
echo "Creating spiceroute namespace..."
kubectl apply -f k8s/namespace.yaml

# Create secrets
echo "Creating secrets..."
kubectl apply -f k8s/secrets.yaml

# Deploy MongoDB
echo "Deploying MongoDB..."
kubectl apply -f k8s/mongodb.yaml

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
kubectl wait --for=condition=ready pod -l app=mongodb -n spiceroute --timeout=300s

# Deploy Elasticsearch
echo "Deploying Elasticsearch..."
kubectl apply -f k8s/elasticsearch.yaml

# Wait for Elasticsearch to be ready
echo "Waiting for Elasticsearch to be ready..."
kubectl wait --for=condition=ready pod -l app=elasticsearch -n spiceroute --timeout=300s

# Deploy the main application
echo "Deploying SpiceRoute.ai application..."
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for the application to be ready
echo "Waiting for SpiceRoute.ai application to be ready..."
kubectl wait --for=condition=ready pod -l app=spiceroute -n spiceroute --timeout=300s

# Get the application URL
echo "Getting application URL..."
minikube service spiceroute-api -n spiceroute --url

echo "Deployment completed!" 