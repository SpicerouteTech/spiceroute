# Private Credentials Documentation
⚠️ DO NOT COMMIT THIS FILE TO GIT ⚠️

## MongoDB Credentials

### Application-level Credentials
- Username: `spiceroute`
- Password: `spiceroute123`
- Connection string: `mongodb://spiceroute:spiceroute123@mongodb:27017`

### Root-level Credentials
- Username: `admin`
- Password: `change-me-in-production`

## Kubernetes Secret Files

### mongodb-secrets.yaml
```yaml
username: c3BpY2Vyb3V0ZQ==  # base64 encoded "spiceroute"
password: c3BpY2Vyb3V0ZTEyMw==  # base64 encoded "spiceroute123"
```

### secrets.yaml
```yaml
mongodb-root-username: admin
mongodb-root-password: change-me-in-production
```

## How to Update Credentials

1. For application-level credentials:
   - Update the base64-encoded values in `mongodb-secrets.yaml`
   - To generate base64: `echo -n "your-password" | base64`

2. For root-level credentials:
   - Update the plaintext values in `secrets.yaml`

3. Apply the changes:
   ```bash
   kubectl apply -f k8s/mongodb-secrets.yaml
   kubectl apply -f k8s/secrets.yaml
   ```

## Security Notes
- Change all default passwords in production
- Use strong, unique passwords
- Rotate credentials regularly
- Keep this file secure and local only 