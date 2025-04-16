# Database Setup Scripts

This directory contains scripts for setting up and managing the MongoDB database schema and collections.

## Prerequisites
- MongoDB 6.0 or higher
- `mongosh` CLI tool
- Kubernetes cluster with MongoDB pod running
- `kubectl` configured with appropriate access

## Available Scripts

### 1. MongoDB Schema Setup
- `mongo-setup.js`: Creates collections with validation and indexes
- `mongo-test-data.js`: Populates database with test data (for development)

## Running the Scripts

### In Kubernetes Environment

1. Copy scripts to MongoDB pod:
```bash
kubectl cp mongo-setup.js spiceroute/mongodb-pod-name:/tmp/
```

2. Execute setup script:
```bash
kubectl exec -it mongodb-pod-name -n spiceroute -- \
  mongosh -u spiceroute -p spiceroute123 \
  --authenticationDatabase admin /tmp/mongo-setup.js
```

### Local Development

1. Start MongoDB locally:
```bash
mongod --dbpath ./data/db
```

2. Run setup script:
```bash
mongosh -u spiceroute -p spiceroute123 \
  --authenticationDatabase admin \
  ./mongo-setup.js
```

## Verification

After running the scripts, verify the setup:

```bash
# Connect to MongoDB
mongosh -u spiceroute -p spiceroute123 --authenticationDatabase admin

# Check collections
use spiceroute
show collections

# Verify indexes
db.store_owners.getIndexes()
db.store_owner_invites.getIndexes()
```

Expected output:
- Two collections: `store_owners` and `store_owner_invites`
- Indexes on both collections
- Schema validation rules active

## Troubleshooting

If you encounter errors:

1. Check MongoDB connection:
```bash
kubectl exec -it mongodb-pod-name -n spiceroute -- mongosh --eval "db.runCommand({ping:1})"
```

2. Verify credentials:
```bash
kubectl get secret mongodb-secrets -n spiceroute -o yaml
```

3. Check MongoDB logs:
```bash
kubectl logs mongodb-pod-name -n spiceroute
``` 