# Notification Service

## Overview
A standalone microservice that handles all notifications across the grocery delivery platform. This service provides a centralized way to manage and send notifications through multiple channels.

## Features
- Multi-channel notification support:
  - Email (SendGrid)
  - SMS (Twilio)
  - WhatsApp (Meta Cloud API)
  - Push Notifications (Firebase Cloud Messaging)
  - In-app notifications
- User notification preferences management
- Push token management for mobile devices
- Notification templates and localization
- Notification history and tracking
- Rate limiting and throttling
- Batch notification support

## Use Cases
1. **Order Updates**
   - Order status changes
   - Delivery updates
   - Substitution notifications
   - Order completion

2. **Marketing & Promotions**
   - Special offers
   - Discounts
   - New store announcements
   - Seasonal promotions
   - Personalized recommendations

3. **User Account**
   - Welcome messages
   - Email verification
   - Password reset
   - Account alerts
   - Profile updates

4. **Store Updates**
   - New items in stock
   - Price changes
   - Store hours updates
   - Holiday schedules

5. **System Notifications**
   - Service updates
   - App updates
   - Maintenance notifications
   - Security alerts

## API Endpoints

### Notification Management
```http
POST /api/v1/notifications/send
POST /api/v1/notifications/send-batch
GET /api/v1/notifications/status/{notification_id}
GET /api/v1/notifications/history
```

### Preferences Management
```http
GET /api/v1/preferences/{user_id}
PUT /api/v1/preferences/{user_id}
PATCH /api/v1/preferences/{user_id}/channels
```

### Device Management
```http
POST /api/v1/devices/register
DELETE /api/v1/devices/unregister
PUT /api/v1/devices/update
GET /api/v1/devices/{user_id}
```

### Templates
```http
POST /api/v1/templates
GET /api/v1/templates/{template_id}
PUT /api/v1/templates/{template_id}
DELETE /api/v1/templates/{template_id}
GET /api/v1/templates/list
```

### Analytics
```http
GET /api/v1/analytics/delivery-rates
GET /api/v1/analytics/engagement
GET /api/v1/analytics/channel-performance
```

## Message Queue Integration
- RabbitMQ/Apache Kafka for asynchronous message processing
- Dead letter queues for failed notifications
- Message replay capability
- Priority queues for urgent notifications

## Configuration
```yaml
notification_service:
  channels:
    email:
      provider: sendgrid
      api_key: ${SENDGRID_API_KEY}
      from_email: notifications@yourdomain.com
      max_retries: 3
    sms:
      provider: twilio
      account_sid: ${TWILIO_ACCOUNT_SID}
      auth_token: ${TWILIO_AUTH_TOKEN}
      from_number: ${TWILIO_NUMBER}
    whatsapp:
      provider: meta
      api_key: ${META_API_KEY}
      phone_number_id: ${META_PHONE_NUMBER_ID}
    push:
      provider: firebase
      api_key: ${FIREBASE_API_KEY}
      project_id: ${FIREBASE_PROJECT_ID}

  rate_limits:
    email:
      per_user: 10/hour
      global: 10000/hour
    sms:
      per_user: 5/hour
      global: 5000/hour
    whatsapp:
      per_user: 5/hour
      global: 5000/hour
    push:
      per_user: 20/hour
      global: 50000/hour

  templates:
    cache_ttl: 3600
    default_locale: en-US
    supported_locales:
      - en-US
      - es-ES
      - fr-FR

  queues:
    message_queue: rabbitmq
    host: ${RABBITMQ_HOST}
    port: ${RABBITMQ_PORT}
    username: ${RABBITMQ_USER}
    password: ${RABBITMQ_PASSWORD}
    vhost: /notifications
```

## Monitoring & Alerts
- Notification delivery rates
- Channel performance metrics
- Error rates and types
- Queue lengths and processing times
- Rate limit usage
- Template usage statistics

## Security
- API authentication using JWT
- Rate limiting per user/IP
- Input validation and sanitization
- PII data encryption
- Audit logging
- GDPR compliance

## High Availability
- Multiple instance deployment
- Queue-based architecture
- Automatic failover
- Load balancing
- Circuit breakers for external services

## Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start development server
uvicorn main:app --reload

# Run linting
flake8 .

# Generate API documentation
python scripts/generate_docs.py
``` 