// Switch to spiceroute database
db = db.getSiblingDB('spiceroute');

// Create store_owners collection with schema validation
db.createCollection('store_owners', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "full_name", "oauth_provider", "oauth_id", "status"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        full_name: {
          bsonType: "string",
          minLength: 1
        },
        phone_number: {
          bsonType: ["string", "null"]
        },
        status: {
          enum: ["pending", "active", "suspended"]
        },
        oauth_provider: {
          enum: ["google", "facebook"]
        },
        oauth_id: {
          bsonType: "string"
        },
        is_verified: {
          bsonType: "bool"
        },
        last_login: {
          bsonType: ["date", "null"]
        },
        created_at: {
          bsonType: "date"
        },
        updated_at: {
          bsonType: "date"
        }
      }
    }
  }
});

// Create store_owner_invites collection with schema validation
db.createCollection('store_owner_invites', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "invited_by", "token", "expires_at", "is_used"],
      properties: {
        email: {
          bsonType: "string",
          pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        },
        invited_by: {
          bsonType: "string"
        },
        token: {
          bsonType: "string"
        },
        expires_at: {
          bsonType: "date"
        },
        is_used: {
          bsonType: "bool"
        },
        created_at: {
          bsonType: "date"
        }
      }
    }
  }
});

// Create indexes
db.store_owners.createIndex({ "email": 1 }, { unique: true });
db.store_owners.createIndex({ "oauth_provider": 1, "oauth_id": 1 }, { unique: true });
db.store_owner_invites.createIndex({ "token": 1 }, { unique: true });
db.store_owner_invites.createIndex({ "email": 1 });
db.store_owner_invites.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });

// Print collections
print("Collections created:");
db.getCollectionNames().forEach(printjson);

// Print indexes
print("\nIndexes for store_owners:");
db.store_owners.getIndexes().forEach(printjson);
print("\nIndexes for store_owner_invites:");
db.store_owner_invites.getIndexes().forEach(printjson); 