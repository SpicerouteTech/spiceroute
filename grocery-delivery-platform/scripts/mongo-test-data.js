// Switch to spiceroute database
db = db.getSiblingDB('spiceroute');

// Sample store owners
const storeOwners = [
  {
    email: "test.owner1@spiceroute.ai",
    full_name: "Test Owner One",
    phone_number: "+1234567890",
    status: "active",
    oauth_provider: "google",
    oauth_id: "123456789",
    is_verified: true,
    last_login: new Date(),
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    email: "test.owner2@spiceroute.ai",
    full_name: "Test Owner Two",
    status: "pending",
    oauth_provider: "facebook",
    oauth_id: "987654321",
    is_verified: false,
    created_at: new Date(),
    updated_at: new Date()
  }
];

// Sample invites
const storeOwnerInvites = [
  {
    email: "new.owner1@spiceroute.ai",
    invited_by: "test.owner1@spiceroute.ai",
    token: "test-token-1",
    expires_at: new Date(Date.now() + 7*24*60*60*1000), // 7 days from now
    is_used: false,
    created_at: new Date()
  },
  {
    email: "new.owner2@spiceroute.ai",
    invited_by: "test.owner1@spiceroute.ai",
    token: "test-token-2",
    expires_at: new Date(Date.now() + 7*24*60*60*1000), // 7 days from now
    is_used: false,
    created_at: new Date()
  }
];

// Clear existing test data
print("Clearing existing test data...");
db.store_owners.deleteMany({ email: /^test\./ });
db.store_owner_invites.deleteMany({ email: /^new\./ });

// Insert store owners
print("Inserting test store owners...");
try {
  const ownerResult = db.store_owners.insertMany(storeOwners);
  print(`Inserted ${ownerResult.insertedCount} store owners`);
} catch (e) {
  print("Error inserting store owners:");
  print(e);
}

// Insert invites
print("Inserting test invites...");
try {
  const inviteResult = db.store_owner_invites.insertMany(storeOwnerInvites);
  print(`Inserted ${inviteResult.insertedCount} invites`);
} catch (e) {
  print("Error inserting invites:");
  print(e);
}

// Verify data
print("\nVerifying inserted data:");
print("\nStore Owners:");
db.store_owners.find({ email: /^test\./ }).forEach(printjson);
print("\nInvites:");
db.store_owner_invites.find({ email: /^new\./ }).forEach(printjson); 