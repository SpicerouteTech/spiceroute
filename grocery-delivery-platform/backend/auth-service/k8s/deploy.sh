#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

echo -e "${BLUE}Deploying Auth Service to Kubernetes...${NC}\n"

# Build Docker image
echo -e "${BLUE}Building Docker image...${NC}"
docker build -t auth-service:1.0.0 ..

# Create namespace if it doesn't exist
echo -e "\n${BLUE}Creating namespace...${NC}"
kubectl apply -f namespace.yaml

# Apply ConfigMap and Secrets
echo -e "\n${BLUE}Applying ConfigMap and Secrets...${NC}"
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml

# Apply Deployment and Service
echo -e "\n${BLUE}Deploying application...${NC}"
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Wait for deployment to be ready
echo -e "\n${BLUE}Waiting for deployment to be ready...${NC}"
kubectl wait --namespace spiceroute \
  --for=condition=ready pod \
  --selector=app=auth-service \
  --timeout=120s

# Check deployment status
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}Deployment successful!${NC}"
    echo -e "\nService endpoints:"
    echo -e "Internal: ${BLUE}auth-service.spiceroute.svc.cluster.local${NC}"
    echo -e "\nTo check the logs:"
    echo -e "${BLUE}kubectl logs -n spiceroute -l app=auth-service${NC}"
else
    echo -e "\n${RED}Deployment failed. Check the logs for more information.${NC}"
    exit 1
fi 