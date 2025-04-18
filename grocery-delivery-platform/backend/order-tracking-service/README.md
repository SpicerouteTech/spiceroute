# Order Tracking Service

## Overview
The Order Tracking Service is a microservice responsible for managing the complete lifecycle of order fulfillment, from initial submission to final delivery. It provides real-time tracking, status updates, and integration with store operations and delivery partners.

## Features
- Real-time order status tracking
- Store acknowledgment and fulfillment tracking
- Delivery partner integration (DoorDash, Uber)
- Order search and filtering capabilities
- Store owner order management
- Real-time notifications
- SLA monitoring

## Search Features
- Advanced order search by:
  - Order ID
  - Customer phone number
  - Customer name
- Search history tracking
- Combined filtering with status and date ranges
- Pagination support
- See [Search Documentation](docs/search.md) for details

## Getting Started

### Prerequisites
- Python 3.11+
- MongoDB 6.0+
- FastAPI
- Motor (async MongoDB driver)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/grocery-delivery-platform.git

# Navigate to the service directory
cd grocery-delivery-platform/backend/order-tracking-service

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Running the Service
```bash
# Development
uvicorn src.main:app --reload

# Production
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## API Documentation
- OpenAPI documentation available at `/docs`
- Detailed API documentation in `/docs` directory
- [Search API Documentation](docs/search.md)

## Architecture
- FastAPI for REST API
- MongoDB for data storage
- Async operations with Motor
- JWT authentication
- Event-driven status updates

## Testing
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src tests/
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details 