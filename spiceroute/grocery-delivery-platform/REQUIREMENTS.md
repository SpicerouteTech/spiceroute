# Database Requirements

## MongoDB Collections

### Store Owners Collection (`store_owners`)

#### Required Fields
- `email`: String, unique, valid email format
- `full_name`: String, non-empty
- `oauth_provider`: Enum ["google", "facebook"]
- `oauth_id`: String
- `status`: Enum ["pending", "active", "suspended"]

#### Optional Fields
- `phone_number`: String or null
- `is_verified`: Boolean
- `last_login`: Date or null
- `created_at`: Date
- `updated_at`: Date

#### Indexes
- Unique index on `email`
- Unique compound index on `oauth_provider` and `oauth_id`

#### Validation Rules
- Email must match standard email format
- Full name must have at least one character
- Status must be one of: pending, active, suspended
- OAuth provider must be either google or facebook

### Store Owner Invites Collection (`store_owner_invites`)

#### Required Fields
- `email`: String, valid email format
- `invited_by`: String
- `token`: String, unique
- `expires_at`: Date
- `is_used`: Boolean
- `created_at`: Date

#### Indexes
- Unique index on `token`
- Index on `email`
- TTL index on `expires_at` (auto-deletes expired invites)

#### Validation Rules
- Email must match standard email format
- Token must be unique
- Invites automatically expire based on `expires_at`
- `is_used` tracks whether the invite has been claimed

## Security Considerations

### Authentication
- Application uses dedicated MongoDB user with limited permissions
- Credentials stored in Kubernetes secrets
- Connection string format: `mongodb://<username>:<password>@mongodb:27017`

### Data Integrity
- Schema validation enforced at database level
- Unique constraints prevent duplicate entries
- TTL index ensures automatic cleanup of expired invites

## Performance Considerations

### Indexing Strategy
- Email and OAuth lookups optimized with indexes
- Compound index for OAuth provider + ID queries
- TTL index manages invite expiration automatically

### Data Types
- Dates stored in native MongoDB format
- Boolean flags for status tracking
- String fields with validation for data consistency 