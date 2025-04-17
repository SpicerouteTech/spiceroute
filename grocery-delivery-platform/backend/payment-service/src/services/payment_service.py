from datetime import datetime
from typing import Optional, List
import httpx
from motor.motor_asyncio import AsyncIOMotorDatabase

from ..models.payment import (
    Transaction, PaymentDistribution, PaymentAudit,
    PaymentStatus, PaymentType, PaymentPartyType, PaymentSummary
)
from ..config import settings

class PaymentService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.transactions = db.transactions
        self.audits = db.payment_audits
        self.toast_client = httpx.AsyncClient(
            base_url=settings.TOAST_API_URL,
            headers={"Authorization": f"Bearer {settings.TOAST_API_KEY}"}
        )
    
    async def init_indexes(self):
        """Initialize database indexes"""
        await self.transactions.create_index("order_id")
        await self.transactions.create_index("cart_id")
        await self.transactions.create_index([("created_at", -1)])
        await self.audits.create_index("transaction_id")
        await self.audits.create_index([("created_at", -1)])
    
    async def create_audit(self, transaction_id: str, event_type: str, status: PaymentStatus, amount: float, metadata: dict = None):
        """Create payment audit record"""
        audit = PaymentAudit(
            transaction_id=transaction_id,
            event_type=event_type,
            status=status,
            amount=amount,
            metadata=metadata or {}
        )
        await self.audits.insert_one(audit.dict())
        return audit
    
    async def process_toast_payment(self, cart_id: str, order_id: str, payment_token: str, amount: float) -> Transaction:
        """Process payment through Toast"""
        try:
            # Create Toast payment request
            response = await self.toast_client.post("/payments", json={
                "amount": int(amount * 100),  # Convert to cents
                "currency": "USD",
                "payment_token": payment_token,
                "description": f"Order {order_id}",
                "metadata": {
                    "cart_id": cart_id,
                    "order_id": order_id
                }
            })
            response.raise_for_status()
            payment_data = response.json()
            
            # Create transaction record
            transaction = Transaction(
                order_id=order_id,
                cart_id=cart_id,
                payment_type=PaymentType.CHARGE,
                payment_method="toast",
                amount=amount,
                status=PaymentStatus.COMPLETED if payment_data["status"] == "succeeded" else PaymentStatus.FAILED,
                metadata=payment_data
            )
            
            if transaction.status == PaymentStatus.COMPLETED:
                # Calculate payment distribution
                summary = PaymentSummary.calculate(
                    subtotal=amount - payment_data.get("delivery_fee", 0),
                    delivery_fee=payment_data.get("delivery_fee", 0)
                )
                
                # Create distribution records
                transaction.distributions = [
                    PaymentDistribution(
                        party_id=payment_data["store_id"],
                        party_type=PaymentPartyType.STORE,
                        amount=summary.store_amount
                    ),
                    PaymentDistribution(
                        party_id=payment_data["delivery_service_id"],
                        party_type=PaymentPartyType.DELIVERY_SERVICE,
                        amount=summary.delivery_fee
                    ),
                    PaymentDistribution(
                        party_id="platform",
                        party_type=PaymentPartyType.PLATFORM,
                        amount=summary.platform_fee
                    )
                ]
                
                transaction.completed_at = datetime.utcnow()
            else:
                transaction.error_message = payment_data.get("error", {}).get("message")
            
            # Save transaction
            await self.transactions.insert_one(transaction.dict())
            
            # Create audit record
            await self.create_audit(
                transaction_id=transaction.id,
                event_type="payment_processed",
                status=transaction.status,
                amount=amount,
                metadata=payment_data
            )
            
            return transaction
            
        except Exception as e:
            # Create failed transaction record
            transaction = Transaction(
                order_id=order_id,
                cart_id=cart_id,
                payment_type=PaymentType.CHARGE,
                payment_method="toast",
                amount=amount,
                status=PaymentStatus.FAILED,
                error_message=str(e)
            )
            await self.transactions.insert_one(transaction.dict())
            
            # Create audit record
            await self.create_audit(
                transaction_id=transaction.id,
                event_type="payment_failed",
                status=PaymentStatus.FAILED,
                amount=amount,
                metadata={"error": str(e)}
            )
            
            raise
    
    async def process_payout(self, distribution: PaymentDistribution) -> bool:
        """Process payout to store or delivery service"""
        try:
            # Create Toast payout request
            response = await self.toast_client.post("/payouts", json={
                "amount": int(distribution.amount * 100),  # Convert to cents
                "currency": "USD",
                "destination": distribution.party_id,
                "description": f"Payout for {distribution.party_type.value}"
            })
            response.raise_for_status()
            payout_data = response.json()
            
            # Update distribution status
            distribution.status = PaymentStatus.COMPLETED
            distribution.payout_id = payout_data["id"]
            distribution.completed_at = datetime.utcnow()
            
            # Create audit record
            await self.create_audit(
                transaction_id=distribution.payout_id,
                event_type="payout_processed",
                status=PaymentStatus.COMPLETED,
                amount=distribution.amount,
                metadata=payout_data
            )
            
            return True
            
        except Exception as e:
            # Create audit record
            await self.create_audit(
                transaction_id=distribution.id,
                event_type="payout_failed",
                status=PaymentStatus.FAILED,
                amount=distribution.amount,
                metadata={"error": str(e)}
            )
            return False
    
    async def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID"""
        data = await self.transactions.find_one({"id": transaction_id})
        return Transaction(**data) if data else None
    
    async def get_transaction_audits(self, transaction_id: str) -> List[PaymentAudit]:
        """Get audit records for a transaction"""
        cursor = self.audits.find({"transaction_id": transaction_id}).sort("created_at", 1)
        return [PaymentAudit(**doc) async for doc in cursor]

# Create service instance
payment_service = None

async def init_payment_service(db: AsyncIOMotorDatabase):
    global payment_service
    payment_service = PaymentService(db)
    await payment_service.init_indexes() 