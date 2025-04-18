# Order Tracking and Notification Services Documentation

## Overview
The Order Tracking and Notification Services are core components of the grocery delivery platform that handle:
1. Real-time order status tracking
2. Multi-channel customer notifications
3. Delivery driver tracking
4. Store acknowledgment management
5. Substitution handling

## Services Architecture

### Order Tracking Service
The Order Tracking Service manages the lifecycle of orders from submission to delivery.

#### Key Features
- Real-time order status updates
- Store acknowledgment monitoring
- Driver location tracking
- Substitution management
- Delivery provider integration (Uber, DoorDash)
- Automatic timeout handling

#### Order States
```
SUBMITTED → STORE_NOTIFIED → STORE_ACKNOWLEDGED → PICKING_IN_PROGRESS 
→ [SUBSTITUTIONS_NEEDED] → READY_FOR_PICKUP → DRIVER_ASSIGNED 
→ DRIVER_PICKUP_COMPLETE → IN_TRANSIT → DELIVERED
```

### Notification Service
The Notification Service handles all customer communications across multiple channels.

#### Supported Channels
- Email (SendGrid)
- SMS (Twilio)
- WhatsApp (Meta Cloud API)
- Push Notifications (Firebase Cloud Messaging)

#### Features
- Channel preference management
- Push token registration/management
- WhatsApp opt-in/opt-out
- Notification logging and tracking
- Delivery status updates

## API Endpoints

### Order Tracking Endpoints

#### Order Management
```http
POST /orders/tracking/init
GET /orders/tracking/{order_id}
PUT /orders/tracking/{order_id}/status
```

#### Store Operations
```http
POST /orders/tracking/{order_id}/acknowledge
PUT /orders/tracking/{order_id}/substitutions
```

#### Delivery Operations
```http
PUT /orders/tracking/{order_id}/driver
PUT /orders/tracking/{order_id}/location
PUT /orders/tracking/{order_id}/delivered
```

### Notification Endpoints

#### Preferences Management
```http
GET /notifications/preferences
PUT /notifications/preferences
```

#### Push Notifications
```http
POST /notifications/push/register-token
DELETE /notifications/push/unregister-token
```

#### WhatsApp Integration
```http
POST /notifications/whatsapp/opt-in
POST /notifications/whatsapp/opt-out
```

## Data Models

### OrderTracking
```python
{
    "order_id": str,
    "store_id": str,
    "customer_id": str,
    "current_status": OrderTrackingStatus,
    "delivery_provider": DeliveryProvider,
    "status_history": List[OrderStatusUpdate],
    "driver_details": Optional[DriverDetails],
    "driver_location": Optional[GeoLocation],
    "substitutions": List[ItemSubstitution],
    "metadata": Dict[str, Any]
}
```

### NotificationPreference
```python
{
    "customer_id": str,
    "channels": List[str],
    "email": Optional[str],
    "phone": Optional[str],
    "push_tokens": List[str],
    "whatsapp_opted_in": bool
}
```

## Database Schema

### MongoDB Collections
- `order_tracking`: Stores order tracking information
- `notification_preferences`: Customer notification preferences
- `push_tokens`: Device tokens for push notifications
- `notification_logs`: Notification delivery logs

### Indexes
```javascript
// Order Tracking Indexes
{ "order_id": 1 }  // unique
{ "store_id": 1 }
{ "customer_id": 1 }
{ "current_status": 1 }
{ "delivery_provider": 1 }
{ "created_at": 1 }

// Notification Indexes
{ "customer_id": 1 }  // unique for preferences
{ "customer_id": 1, "token": 1 }  // unique for push tokens
{ "customer_id": 1, "sent_at": -1 }  // for notification logs
```

## Error Handling

### Common Error Scenarios
- Store acknowledgment timeout
- Invalid order state transitions
- Notification delivery failures
- Push token registration conflicts
- Delivery provider integration errors

### Error Response Format
```json
{
    "detail": "Error description",
    "code": "ERROR_CODE",
    "timestamp": "ISO-8601 timestamp",
    "path": "/api/endpoint"
}
```

## Configuration

### Required Environment Variables
```bash
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=grocery_delivery

# Notification Providers
SENDGRID_API_KEY=your_sendgrid_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
META_API_KEY=your_meta_api_key
FIREBASE_API_KEY=your_firebase_key

# Delivery Providers
UBER_API_KEY=your_uber_key
DOORDASH_API_KEY=your_doordash_key
```

## Monitoring and Logging

### Key Metrics
- Order state transition times
- Store acknowledgment rates
- Delivery completion rates
- Notification delivery success rates
- Channel-specific metrics

### Log Levels
- ERROR: Service failures and exceptions
- WARN: Timeouts and retryable errors
- INFO: State transitions and notifications
- DEBUG: Detailed operation logs

## Security

### Authentication
- JWT-based authentication for all endpoints
- Token validation and refresh mechanism
- Role-based access control

### Data Protection
- Encrypted communication channels
- Secure token storage
- PII data handling compliance
- GDPR compliance measures

## Best Practices

### Order Tracking
1. Always validate state transitions
2. Implement retry mechanisms for provider calls
3. Use timeouts for critical operations
4. Maintain complete audit trails

### Notifications
1. Respect user preferences
2. Implement rate limiting
3. Handle delivery failures gracefully
4. Monitor notification success rates

## Integration Guide

### Adding New Notification Channels
1. Implement provider interface
2. Add channel configuration
3. Update preference management
4. Add notification templates

### Adding New Delivery Providers
1. Implement provider client
2. Add provider configuration
3. Update tracking service
4. Add provider-specific endpoints

## Deployment

### Prerequisites
- MongoDB 4.4+
- Python 3.11+
- Redis (for rate limiting)
- Message Queue (optional)

### Scaling Considerations
- Horizontal scaling capability
- Database sharding strategy
- Caching implementation
- Rate limiting policies 