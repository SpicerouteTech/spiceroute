# Kubernetes to Podman Migration Guide

This directory contains all the necessary files and scripts to migrate your Kubernetes workloads (MongoDB and Elasticsearch) to Podman.

## Prerequisites

1. Podman Desktop installed
2. Lima VM for Podman created and running
3. `podman-compose` installed (`pip3 install podman-compose`)
4. Your Kubernetes workloads still running (for data migration)

## Migration Steps

### Automated Migration

The easiest way to migrate is using the provided script:

```bash
./migrate-to-podman.sh
```

This script will:
1. Check if Podman is running
2. Verify podman-compose is installed
3. Ensure MongoDB secret files are available
4. Start the Podman containers
5. Offer to migrate data from Kubernetes to Podman
6. Offer to clean up Kubernetes resources

### Manual Migration

If you prefer to do things step-by-step:

1. Start the Podman Lima VM:
   ```bash
   limactl start podman
   export DOCKER_HOST=$(limactl info podman socket)
   ```

2. Verify your secrets:
   ```bash
   cat secrets/mongodb-username.txt
   cat secrets/mongodb-password.txt
   ```

3. Start your Podman containers:
   ```bash
   podman-compose up -d
   ```

4. Migrate MongoDB data (optional):
   ```bash
   # Export from Kubernetes
   K8S_MONGO_POD=$(kubectl get pods -n spiceroute -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
   kubectl exec -n spiceroute $K8S_MONGO_POD -- mongodump --out=/tmp/mongodump
   kubectl cp spiceroute/$K8S_MONGO_POD:/tmp/mongodump ./tmp_data/mongodump
   
   # Import to Podman
   PODMAN_MONGO_CONTAINER=$(podman ps --filter name=spiceroute-mongodb -q)
   podman cp ./tmp_data/mongodump $PODMAN_MONGO_CONTAINER:/tmp/
   podman exec $PODMAN_MONGO_CONTAINER mongorestore --username $(cat secrets/mongodb-username.txt) --password $(cat secrets/mongodb-password.txt) --authenticationDatabase admin /tmp/mongodump
   ```

5. Clean up Kubernetes resources (optional):
   ```bash
   kubectl delete -n spiceroute deployment/mongodb deployment/elasticsearch
   kubectl delete -n spiceroute service/mongodb service/elasticsearch
   kubectl delete -n spiceroute pvc/mongodb-pvc pvc/elasticsearch-pvc
   kubectl delete -n spiceroute secret/mongodb-secrets
   ```

## File Structure

- `podman-compose.yml` - Main compose file for Podman
- `secrets/` - Directory containing MongoDB credentials
  - `mongodb-username.txt` - MongoDB username
  - `mongodb-password.txt` - MongoDB password
- `migrate-to-podman.sh` - Migration script
- `mongodb-deploy.yaml` - Exported Kubernetes MongoDB deployment
- `mongodb-svc.yaml` - Exported Kubernetes MongoDB service
- `elasticsearch-deploy.yaml` - Exported Kubernetes Elasticsearch deployment
- `elasticsearch-svc.yaml` - Exported Kubernetes Elasticsearch service
- `mongodb-secrets.yaml` - Exported Kubernetes MongoDB secrets
- `pvcs.yaml` - Exported Kubernetes PVCs

## Managing Your Podman Services

After migration, you can manage your services with:

```bash
# List containers
podman-compose ps

# View logs
podman-compose logs -f

# Stop services
podman-compose down

# Start services
podman-compose up -d
```

You can also use Podman Desktop for a GUI interface to manage your containers.

## Troubleshooting

### Connection Issues
If you can't connect to MongoDB or Elasticsearch, check:
```bash
podman logs spiceroute-mongodb
podman logs spiceroute-elasticsearch
```

### Data Not Migrated Correctly
If data didn't migrate properly:
```bash
# Connect to MongoDB and check
podman exec -it spiceroute-mongodb mongosh -u $(cat secrets/mongodb-username.txt) -p $(cat secrets/mongodb-password.txt) --authenticationDatabase admin
```

### Podman Desktop Not Showing Containers
Try refreshing your connection:
```bash
limactl stop podman
limactl start podman
``` 