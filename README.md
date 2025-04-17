# SpiceRoute Grocery Delivery Platform

A modern grocery delivery platform built with FastAPI, MongoDB, Redis, and React.

## Project Structure

```
grocery-delivery-platform/
├── backend/
│   └── store-service/      # Store management service
├── frontend/              # React frontend application
├── k8s/                  # Kubernetes manifests
└── scripts/              # Utility scripts
```

## Development Setup

### Prerequisites

- Git
- GitHub account with repository access
- Kubernetes cluster (local or remote)
- kubectl CLI tool
- GitHub CLI (optional)

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spiceroute.git
cd spiceroute
```

2. Create a GitHub Personal Access Token (PAT):
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `read:packages` and `write:packages` permissions
   - Save the token securely

3. Configure GitHub Container Registry authentication:
```bash
echo $GITHUB_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

### Local Kubernetes Setup

1. Install required tools:
```bash
# For macOS
brew install kubectl kind

# For Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

2. Create a local Kubernetes cluster:
```bash
kind create cluster --name spiceroute
```

3. Create the namespace and secrets:
```bash
kubectl create namespace spiceroute

# Create MongoDB credentials secret
kubectl create secret generic mongodb-credentials \
  --namespace spiceroute \
  --from-literal=uri="mongodb://username:password@mongodb:27017/spiceroute"

# Create Redis credentials secret
kubectl create secret generic redis-credentials \
  --namespace spiceroute \
  --from-literal=uri="redis://redis:6379/0"
```

### Deployment

The GitHub Actions workflows will:
1. Run tests and build Docker images on push to main
2. Generate Kubernetes manifests
3. Create a PR with updated manifests

To deploy manually:

1. Apply the generated manifests:
```bash
kubectl apply -f k8s-generated/
```

2. Verify the deployment:
```bash
kubectl get pods -n spiceroute
kubectl get services -n spiceroute
```

## Contributing

1. Create a new branch for your feature:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Add your feature description"
```

3. Push to GitHub:
```bash
git push origin feature/your-feature-name
```

4. Create a Pull Request on GitHub

## License

This project is licensed under the MIT License - see the LICENSE file for details. 