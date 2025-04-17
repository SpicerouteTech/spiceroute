#!/bin/bash

# Create namespace if it doesn't exist
kubectl create namespace spiceroute --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kong
kubectl apply -f k8s/kong-deployment.yaml
kubectl apply -f k8s/kong-service.yaml
kubectl apply -f k8s/kong-config.yaml

# Wait for Kong to be ready
echo "Waiting for Kong to be ready..."
kubectl wait --namespace spiceroute \
  --for=condition=ready pod \
  --selector=app=kong \
  --timeout=90s

# Get Kong admin URL
KONG_ADMIN_IP=$(kubectl get svc -n spiceroute kong-admin -o jsonpath='{.spec.clusterIP}')
echo "Kong Admin API is available at: http://$KONG_ADMIN_IP:8001"

# Get Kong proxy URL
KONG_PROXY_IP=$(kubectl get svc -n spiceroute kong-proxy -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Kong Proxy is available at: http://$KONG_PROXY_IP"

# Apply Kong configuration
echo "Applying Kong configuration..."
kubectl exec -n spiceroute $(kubectl get pod -n spiceroute -l app=kong -o jsonpath='{.items[0].metadata.name}') -- kong config db_import /etc/kong/kong.yml

echo "Kong deployment completed!" 