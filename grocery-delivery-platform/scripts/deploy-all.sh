#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Full Deployment Process for Spiceroute ---"

# --- Configuration ---
NAMESPACE="spiceroute"
K8S_DIR="../k8s" # Relative path from script location
AUTH_SERVICE_K8S_DIR="../backend/auth-service/k8s" # Relative path
STORE_SERVICE_K8S_DIR="../backend/store-service/k8s" # Relative path
CATALOG_SERVICE_K8S_DIR="../backend/catalog-service/k8s" # Relative path

# --- 1. Ensure Namespace Exists ---
echo "[1/8] Ensuring namespace '$NAMESPACE' exists..."
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# --- 2. Apply Secrets ---
# Order matters: Apply secrets before deployments that need them.
echo "[2/8] Applying secrets..."
kubectl apply -f "$K8S_DIR/mongodb-secrets.yaml" -n "$NAMESPACE"
# Add other secrets files here if created later (e.g., general app secrets, other service secrets)
# kubectl apply -f "$K8S_DIR/secrets.yaml" -n "$NAMESPACE" # Example

# --- 3. Apply Persistent Volume Claims ---
echo "[3/8] Applying Persistent Volume Claims..."
kubectl apply -f "$K8S_DIR/mongodb-pvc.yaml" -n "$NAMESPACE"
kubectl apply -f "$K8S_DIR/elasticsearch-pvc.yaml" -n "$NAMESPACE"

# --- 4. Apply ConfigMaps ---
echo "[4/8] Applying ConfigMaps..."
kubectl apply -f "$K8S_DIR/kong-config.yaml" -n "$NAMESPACE"
# Add other ConfigMap files here if created later
# kubectl apply -f "$AUTH_SERVICE_K8S_DIR/configmap.yaml" -n "$NAMESPACE" # Example for auth-service if needed

# --- 5. Deploy Dependencies (MongoDB, Elasticsearch) ---
echo "[5/8] Deploying dependencies (MongoDB, Elasticsearch)..."
kubectl apply -f "$K8S_DIR/mongodb-deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$K8S_DIR/mongodb-service.yaml" -n "$NAMESPACE"
kubectl apply -f "$K8S_DIR/elasticsearch-deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$K8S_DIR/elasticsearch-service.yaml" -n "$NAMESPACE"

# --- 6. Deploy API Gateway (Kong) ---
echo "[6/8] Deploying API Gateway (Kong)..."
# Note: Kong deployment is configured to use KONG_DECLARATIVE_CONFIG with the mounted kong-config.yaml
kubectl apply -f "$K8S_DIR/kong-deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$K8S_DIR/kong-service.yaml" -n "$NAMESPACE"

# --- 7. Deploy Application Microservices ---
echo "[7/8] Deploying application microservices..."
# Auth Service
echo "   - Deploying Auth Service..."
kubectl apply -f "$AUTH_SERVICE_K8S_DIR/deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$AUTH_SERVICE_K8S_DIR/service.yaml" -n "$NAMESPACE"

# Store Service
echo "   - Deploying Store Service..."
kubectl apply -f "$STORE_SERVICE_K8S_DIR/deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$STORE_SERVICE_K8S_DIR/service.yaml" -n "$NAMESPACE"

# Catalog Service
echo "   - Deploying Catalog Service..."
kubectl apply -f "$CATALOG_SERVICE_K8S_DIR/deployment.yaml" -n "$NAMESPACE"
kubectl apply -f "$CATALOG_SERVICE_K8S_DIR/service.yaml" -n "$NAMESPACE"

# Add deployments/services for frontend-service here later
# echo "   - Deploying Frontend Service..." # If frontend runs in K8s
# kubectl apply -f "../frontend/k8s/deployment.yaml" -n "$NAMESPACE"
# kubectl apply -f "../frontend/k8s/service.yaml" -n "$NAMESPACE"

# --- 8. Wait for Deployments & Run Tests ---
echo "[8/8] Waiting for critical deployments to be ready..."

echo "   - Waiting for MongoDB..."
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=mongodb --timeout=180s

echo "   - Waiting for Elasticsearch..."
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=elasticsearch --timeout=180s

echo "   - Waiting for Kong..."
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=kong --timeout=120s

echo "   - Waiting for Auth Service..."
# Make sure the selector 'app=auth-service' matches the label in auth-service/k8s/deployment.yaml
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=auth-service --timeout=120s

echo "   - Waiting for Store Service..."
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=store-service --timeout=120s

echo "   - Waiting for Catalog Service..."
kubectl wait --namespace "$NAMESPACE" --for=condition=ready pod --selector=app=catalog-service --timeout=120s

# Add waits for other application services if needed

echo "--- Running Tests (Placeholder) ---"
# TODO: Implement actual test execution logic.
# This could involve running a dedicated test pod/job in Kubernetes,
# or running scripts from the host machine that are configured to
# target the services exposed via Kong or NodePorts/LoadBalancers.
# Example: kubectl apply -f path/to/test-job.yaml -n $NAMESPACE
# Example: cd ../tests && ./run-integration-tests.sh --kube-context=$(kubectl config current-context)
echo "(Skipping tests for now)"
echo "--- Test Placeholder End ---"


# --- Deployment Summary ---
echo "-----------------------------------------------------"
echo "Deployment script finished."
echo "-----------------------------------------------------"
echo "Access points:"

# Attempt to get Kong Proxy LoadBalancer IP (might take time)
echo "Attempting to get Kong Proxy LoadBalancer IP (may take a moment)..."
KONG_PROXY_IP=$(kubectl get svc -n "$NAMESPACE" kong-proxy -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || echo "")
if [[ -n "$KONG_PROXY_IP" ]]; then
  echo "  Kong Proxy URL: http://$KONG_PROXY_IP"
  echo "  Auth Service: http://$KONG_PROXY_IP/auth"
  echo "  Store Profile Service: http://$KONG_PROXY_IP/store"
  echo "  Catalog Service: http://$KONG_PROXY_IP/catalog"
else
  echo "  Kong Proxy LoadBalancer IP is pending or not available."
  # Fallback to NodePort if LoadBalancer IP isn't assigned
  KONG_NODE_PORT=$(kubectl get svc -n "$NAMESPACE" kong-proxy -o jsonpath='{.spec.ports[?(@.name=="proxy")].nodePort}' 2>/dev/null || echo "")
  if [[ -n "$KONG_NODE_PORT" ]]; then
     # Try to get a node IP (this is a best guess, might not work in all K8s setups)
     NODE_IP=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}' 2>/dev/null || kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="ExternalIP")].address}' 2>/dev/null || echo "NODE_IP_UNKNOWN")
     if [[ "$NODE_IP" != "NODE_IP_UNKNOWN" ]]; then
        echo "  Alternatively, try accessing via NodePort: http://$NODE_IP:$KONG_NODE_PORT"
        echo "  Auth Service: http://$NODE_IP:$KONG_NODE_PORT/auth"
        echo "  Store Profile Service: http://$NODE_IP:$KONG_NODE_PORT/store"
        echo "  Catalog Service: http://$NODE_IP:$KONG_NODE_PORT/catalog"
     else
        echo "  Could not determine Node IP for NodePort access. NodePort is: $KONG_NODE_PORT"
     fi
  fi
fi

# Kong Admin URL (Internal ClusterIP)
KONG_ADMIN_IP=$(kubectl get svc -n "$NAMESPACE" kong-admin -o jsonpath='{.spec.clusterIP}' 2>/dev/null || echo "")
if [[ -n "$KONG_ADMIN_IP" ]]; then
   echo "  Kong Admin API (ClusterIP): http://$KONG_ADMIN_IP:8001"
fi

echo "-----------------------------------------------------" 