# Order Search Documentation

## Overview
The Order Search feature allows store owners to efficiently search and filter orders using various criteria. This document outlines the available search capabilities, API endpoints, and implementation details.

## Search Features

### Search Criteria
- **Order ID**: Search by exact or partial order ID
- **Customer Phone**: Search by customer's phone number
- **Customer Name**: Search by customer's name
- **Combined Filtering**: Combine search with status and date range filters

### Search Capabilities
- Case-insensitive search
- Partial matching support
- Recent search history tracking
- Pagination support
- Combined filtering with existing order filters

## API Endpoints

### Search Orders
```http
GET /store/orders/search
```

**Query Parameters:**
- `query` (required): Search term
- `search_type` (required): One of ["order_id", "phone", "customer_name"]
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "orders": [
    {
      "order_id": "string",
      "customer_details": {
        "name": "string",
        "phone": "string"
      },
      // ... other order fields
    }
  ],
  "total": 0,
  "page": 1,
  "page_size": 20,
  "total_pages": 0,
  "search_type": "string",
  "search_query": "string"
}
```

### Recent Searches
```http
GET /store/orders/search/recent
```

**Query Parameters:**
- `limit` (optional): Number of recent searches to return (default: 5, max: 20)

**Response:**
```json
[
  {
    "_id": "search_query",
    "last_used": "timestamp",
    "count": 0
  }
]
```

### Combined Search with Filters
```http
GET /store/orders
```

**Query Parameters:**
- `search_query` (optional): Search term
- `search_type` (optional): One of ["order_id", "phone", "customer_name"]
- `status` (optional): List of order statuses
- `start_date` (optional): Filter orders from this date
- `end_date` (optional): Filter orders until this date
- `page` (optional): Page number
- `page_size` (optional): Items per page

## Implementation Details

### Search History
- Stores up to 50 most recent searches per store
- Tracks:
  - Search query
  - Search type
  - Timestamp
  - Usage count

### Performance Considerations
- Uses MongoDB text indexes for efficient searching
- Implements pagination to handle large result sets
- Caches recent searches for quick access

### Security
- All endpoints require store owner authentication
- Search results are scoped to the authenticated store
- Input validation for all search parameters

## Usage Examples

### Basic Search
```typescript
const response = await fetch(
  '/store/orders/search?query=ORD123&search_type=order_id',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);
```

### Combined Search with Filters
```typescript
const params = new URLSearchParams({
  search_query: 'John',
  search_type: 'customer_name',
  status: 'DELIVERED',
  start_date: '2024-01-01'
});

const response = await fetch(
  `/store/orders?${params.toString()}`,
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);
```

### Recent Searches
```typescript
const response = await fetch(
  '/store/orders/search/recent?limit=10',
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);
```

## Error Handling

### Common Error Codes
- `400 Bad Request`: Invalid search parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Store not authorized to access orders
- `422 Unprocessable Entity`: Invalid search type or query format

### Error Response Format
```json
{
  "detail": "Error message describing the issue"
}
```

## Best Practices
1. Always specify search type for better performance
2. Use pagination for large result sets
3. Implement proper error handling
4. Cache frequently used search results
5. Monitor search performance metrics 