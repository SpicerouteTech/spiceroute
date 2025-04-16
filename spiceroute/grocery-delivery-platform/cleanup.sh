#!/bin/bash

# Delete all resources in the spiceroute namespace
echo "Deleting all resources in spiceroute namespace..."
kubectl delete all --all -n spiceroute
kubectl delete pvc --all -n spiceroute
kubectl delete secrets --all -n spiceroute
kubectl delete namespace spiceroute

# Stop Minikube
echo "Stopping Minikube..."
minikube stop

echo "Cleanup completed!" 