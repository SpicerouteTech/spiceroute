# SpiceRoute.ai

A modern AI-powered platform for authentic Indian groceries and spices delivery.

## MVP Overview

This initial version focuses on launching with a single Indian grocery store partner and limited geographic coverage. The MVP will establish core functionality for customers to browse, search, order, and receive deliveries while providing the store owner with basic management tools. The platform will be available via both web and mobile interfaces to maximize accessibility.

## Core Features

### Customer Experience
- Authentication & Onboarding via Google/Facebook
- Store Discovery & Browsing
- Product Catalog
- Shopping Cart Management
- Order Processing & Tracking
- Multiple Delivery Addresses
- Payment Method Management
- Real-time Order Status Updates
- Notifications

### Store Manager Experience
- Store Setup & Management
- Inventory Management
- Order Management
- Basic Analytics
- Product Catalog Management
- Store Profile Management

### Admin Portal
- User Management
- Store Management
- Order Oversight
- Platform Analytics

## Technical Stack

### Frontend
- React for web front-end
- React Native for mobile apps
- Progressive Web App capabilities
- Responsive design

### Backend Services

#### Store Owner Service
- Authentication Service (OAuth with Google/Facebook)
- Store Profile Management
- Catalog Management Service
- Inventory Management
- Order Fulfillment

#### Consumer Service
- Authentication Service (OAuth with Google/Facebook)
- Profile Management
  - Multiple delivery addresses
  - Payment methods
  - Order history
- Shopping Service
  - Cart management
  - Order processing
  - Order tracking
- Product Browsing & Search

#### Shared Services
- Search Service
- Payment Service
- Delivery Service
- Notification Service

### Data Architecture
- MongoDB for flexible data storage
- Elasticsearch for search functionality
- AWS infrastructure (ECS, S3, SQS, SNS)

### Database Schema

#### Store Management
- `store_owners`: Manages store owner accounts
  - OAuth-based authentication (Google/Facebook)
  - Email verification and status tracking
  - Unique constraints on email and OAuth IDs
  
- `store_owner_invites`: Handles invitation system
  - Secure token-based invites
  - Automatic expiration via TTL index
  - Tracks invite usage and creation

#### Consumer Management
- `consumers`: Manages consumer accounts
  - OAuth-based authentication (Google/Facebook)
  - Profile information
  - Multiple delivery addresses
  - Payment methods
  - Shopping cart
  - Order history

- `orders`: Manages order lifecycle
  - Order details and items
  - Delivery information
  - Payment information
  - Status tracking
  - Timestamps

For detailed database requirements and validation rules, see [REQUIREMENTS.md](./REQUIREMENTS.md).

### Infrastructure
- Kubernetes for container orchestration
- Podman for container runtime
- GitHub Actions for CI/CD
- Cloud-based SaaS deployment

## Development Approach
- Acceptance Test-Driven Development (ATDD)
- Modular microservices architecture
- Schema validation and human review
- Comprehensive testing strategy

### Testing
The platform includes automated testing for all services:
- Unit tests for individual components
- Integration tests for service interactions
- API tests to validate endpoints

To run all tests:
```bash
./scripts/run_tests.sh
```

## Services Details

### Store Owner Service
The Store Owner Service manages store operations:
- Store profile management
- Product catalog CRUD operations
- Inventory management
- Order fulfillment
- Business hours and availability
- Location and service area configuration

### Consumer Service
The Consumer Service handles customer interactions:
- Profile management
- Multiple delivery addresses
- Payment methods
- Shopping cart
- Order management
- Order tracking
- Product browsing

## Deployment

### Prerequisites
- Kubernetes cluster
- Podman installed
- kubectl configured
- Container registry access

### Local Development
1. Install Podman
2. Build the container:
   ```bash
   podman build -t spiceroute/api:latest .
   ```

### Database Setup
1. Navigate to the scripts directory:
   ```bash
   cd scripts
   ```

2. Set up MongoDB schema and indexes:
   ```bash
   # In Kubernetes environment
   kubectl cp mongo-setup.js spiceroute/$(kubectl get pod -l app=mongodb -n spiceroute -o jsonpath='{.items[0].metadata.name}'):/tmp/
   kubectl exec -it $(kubectl get pod -l app=mongodb -n spiceroute -o jsonpath='{.items[0].metadata.name}') -n spiceroute -- \
     mongosh -u spiceroute -p spiceroute123 --authenticationDatabase admin /tmp/mongo-setup.js

   # For local development
   mongosh -u spiceroute -p spiceroute123 --authenticationDatabase admin ./mongo-setup.js
   ```

3. (Optional) Load test data:
   ```bash
   # In Kubernetes environment
   kubectl cp mongo-test-data.js spiceroute/$(kubectl get pod -l app=mongodb -n spiceroute -o jsonpath='{.items[0].metadata.name}'):/tmp/
   kubectl exec -it $(kubectl get pod -l app=mongodb -n spiceroute -o jsonpath='{.items[0].metadata.name}') -n spiceroute -- \
     mongosh -u spiceroute -p spiceroute123 --authenticationDatabase admin /tmp/mongo-test-data.js

   # For local development
   mongosh -u spiceroute -p spiceroute123 --authenticationDatabase admin ./mongo-test-data.js
   ```

For detailed information about the database setup scripts and troubleshooting, see [scripts/README.md](./scripts/README.md).

### MongoDB Credentials Configuration
The application uses two sets of MongoDB credentials managed through Kubernetes secrets:

1. Application-level credentials (used by the app to connect to MongoDB)
2. Root-level credentials (used for MongoDB administration)

These credentials are stored in:
- `mongodb-secrets.yaml`: Contains application-level credentials
- `secrets.yaml`: Contains root-level credentials

To update the credentials:
1. Update the values in the respective secret files
2. Apply the changes:
   ```bash
   kubectl apply -f k8s/mongodb-secrets.yaml
   kubectl apply -f k8s/secrets.yaml
   ```

Note: Always use strong, unique passwords in production environments and ensure proper security measures are in place.

### Kubernetes Deployment
1. Create the namespace:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```

2. Deploy MongoDB and Elasticsearch:
   ```bash
   kubectl apply -f k8s/mongodb.yaml
   kubectl apply -f k8s/elasticsearch.yaml
   ```

3. Deploy the services:
   ```bash
   kubectl apply -f k8s/store-service/
   kubectl apply -f k8s/consumer-service/
   ```

4. Deploy Kong API Gateway:
   ```bash
   kubectl apply -f k8s/kong-config.yaml
   kubectl apply -f k8s/kong-deployment.yaml
   ```

### Service Ports
- Store Owner Service: 8000
- Consumer Service: 8001
- MongoDB: 27017
- Elasticsearch: 9200
- Kong API Gateway: 8443 (HTTPS)