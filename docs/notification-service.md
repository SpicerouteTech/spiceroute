# Notification Service Documentation

## Overview
The Notification Service is a standalone microservice that handles all notification-related functionality across the grocery delivery platform. It provides a centralized system for managing and sending notifications through multiple channels, supporting various use cases from order updates to marketing campaigns.

## Architecture

### Core Components
1. **Notification Service**
   - Manages notification dispatch across channels
   - Handles rate limiting and delivery scheduling
   - Processes notification templates
   - Manages campaigns and user segments

2. **Database Service**
   - MongoDB integration for data persistence
   - Manages indexes for optimal performance
   - Handles CRUD operations for all notification entities

3. **Channel Providers**
   - Email (SendGrid)
   - SMS (Twilio)
   - WhatsApp (Meta Cloud API)
   - Push Notifications (Firebase Cloud Messaging)
   - Web Push
   - In-App Notifications

### Data Models

#### Core Models
1. **NotificationTemplate**
   ```python
   {
       "id": "string",
       "name": "string",
       "type": "enum(ORDER_STATUS|PROMOTION|...)",
       "channels": ["email", "sms", ...],
       "templates": {
           "email": {"subject": "...", "body": "..."},
           "sms": {"body": "..."}
       },
       "variables": ["order_id", "customer_name", ...]
   }
   ```

2. **Notification**
   ```python
   {
       "id": "string",
       "user_id": "string",
       "type": "enum(ORDER_STATUS|PROMOTION|...)",
       "channel": "enum(EMAIL|SMS|...)",
       "priority": "enum(LOW|MEDIUM|HIGH|URGENT)",
       "content": {"subject": "...", "body": "..."},
       "status": "enum(PENDING|SENT|DELIVERED|FAILED|READ)"
   }
   ```

3. **NotificationPreference**
   ```python
   {
       "user_id": "string",
       "email": "string",
       "phone": "string",
       "channels": {
           "ORDER_STATUS": ["email", "sms"],
           "PROMOTION": ["email"]
       },
       "quiet_hours": {"start": "22:00", "end": "07:00"},
       "marketing_opted_in": boolean
   }
   ```

## Features

### 1. Multi-Channel Support
- **Email**: Transactional and marketing emails
- **SMS**: Order updates and critical notifications
- **WhatsApp**: Rich messaging with interactive elements
- **Push Notifications**: Mobile app notifications
- **Web Push**: Browser notifications
- **In-App**: Real-time in-application notifications

### 2. Template Management
- Dynamic template variables
- Channel-specific templates
- Localization support
- Template versioning
- Preview functionality

### 3. Campaign Management
- Targeted campaigns based on user segments
- Scheduled campaigns
- A/B testing support
- Campaign analytics and tracking
- Delivery rate monitoring

### 4. User Preferences
- Channel preferences per notification type
- Quiet hours configuration
- Frequency limits
- Marketing opt-in/opt-out
- Device token management

### 5. Rate Limiting & Throttling
- Per-user rate limits
- Channel-specific limits
- Global rate limiting
- Quiet hours enforcement
- Priority-based delivery

## API Endpoints

### Notification Management
```http
POST /api/v1/notifications/send
Request:
{
    "user_id": "string",
    "type": "ORDER_STATUS",
    "template_id": "string",
    "variables": {"order_id": "123", ...},
    "priority": "HIGH"
}

POST /api/v1/notifications/send-batch
GET /api/v1/notifications/{notification_id}/status
GET /api/v1/notifications/history
```

### Template Management
```http
POST /api/v1/templates
GET /api/v1/templates/{template_id}
PUT /api/v1/templates/{template_id}
DELETE /api/v1/templates/{template_id}
```

### Campaign Management
```http
POST /api/v1/campaigns
GET /api/v1/campaigns/{campaign_id}
PUT /api/v1/campaigns/{campaign_id}/status
GET /api/v1/campaigns/{campaign_id}/metrics
```

### Preference Management
```http
GET /api/v1/preferences/{user_id}
PUT /api/v1/preferences/{user_id}
PATCH /api/v1/preferences/{user_id}/channels
```

## Error Handling

### Error Response Format
```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": {}
    },
    "request_id": "string"
}
```

### Common Error Codes
- `RATE_LIMITED`: Rate limit exceeded
- `INVALID_TEMPLATE`: Template validation failed
- `CHANNEL_UNAVAILABLE`: Notification channel unavailable
- `INVALID_PREFERENCE`: Invalid preference configuration
- `CAMPAIGN_ERROR`: Campaign execution error

## Configuration

### Environment Variables
```bash
# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=notifications

# Rate Limits
RATE_LIMIT_EMAIL=100/hour
RATE_LIMIT_SMS=50/hour
RATE_LIMIT_PUSH=200/hour

# Provider API Keys
SENDGRID_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
FIREBASE_API_KEY=your_key
```

## Monitoring

### Key Metrics
1. **Delivery Metrics**
   - Delivery success rate
   - Bounce rate
   - Click-through rate
   - Open rate (for emails)

2. **Performance Metrics**
   - Average delivery time
   - Queue length
   - Error rate
   - API response time

3. **Business Metrics**
   - Notifications by type
   - User engagement
   - Campaign performance
   - Channel effectiveness

### Logging
- Request/Response logging
- Error logging
- Audit logging
- Performance logging

## Security

### Authentication & Authorization
- JWT-based authentication
- Role-based access control
- API key authentication for providers

### Data Protection
- PII encryption
- Secure credential storage
- Data retention policies
- GDPR compliance

## Best Practices

### Implementation Guidelines
1. **Rate Limiting**
   - Implement both user-level and global rate limits
   - Use sliding window rate limiting
   - Consider priority levels

2. **Error Handling**
   - Implement retry mechanisms
   - Use exponential backoff
   - Maintain dead letter queues

3. **Performance**
   - Use appropriate indexes
   - Implement caching
   - Batch operations when possible

4. **Monitoring**
   - Set up alerts for critical errors
   - Monitor delivery rates
   - Track provider health

### Integration Guidelines
1. **Service Integration**
   - Use asynchronous communication
   - Implement circuit breakers
   - Handle partial failures

2. **Provider Integration**
   - Abstract provider implementations
   - Handle provider-specific errors
   - Implement fallback providers

## Deployment

### Prerequisites
- MongoDB 4.4+
- Python 3.9+
- Redis (for rate limiting)
- Message Queue (RabbitMQ/Kafka)

### Installation
```bash
# Clone repository
git clone [repository_url]

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Initialize database
python scripts/init_db.py

# Run migrations
python scripts/migrate.py

# Start service
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Health Checks
```http
GET /health
Response:
{
    "status": "healthy",
    "version": "1.0.0",
    "dependencies": {
        "mongodb": "connected",
        "redis": "connected",
        "providers": {
            "email": "healthy",
            "sms": "healthy"
        }
    }
}
``` 