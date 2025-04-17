from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    TOAST = "toast"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"

class PaymentType(str, Enum):
    CHARGE = "charge"  # Customer payment
    PAYOUT = "payout"  # Payment to store/delivery service

class PaymentPartyType(str, Enum):
    CUSTOMER = "customer"
    STORE = "store"
    DELIVERY_SERVICE = "delivery_service"
    PLATFORM = "platform"

class PaymentDistribution(BaseModel):
    party_id: str = Field(..., description="ID of the receiving party")
    party_type: PaymentPartyType = Field(..., description="Type of the receiving party")
    amount: float = Field(..., gt=0, description="Amount to be distributed")
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    payout_id: Optional[str] = Field(None, description="ID of the payout transaction")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    order_id: str = Field(..., description="Associated order ID")
    cart_id: str = Field(..., description="Associated cart ID")
    payment_type: PaymentType = Field(..., description="Type of payment")
    payment_method: PaymentMethod = Field(..., description="Payment method used")
    amount: float = Field(..., gt=0, description="Total transaction amount")
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    distributions: List[PaymentDistribution] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict, description="Additional payment metadata")
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class PaymentAudit(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    transaction_id: str = Field(..., description="Associated transaction ID")
    event_type: str = Field(..., description="Type of payment event")
    status: PaymentStatus = Field(..., description="Status after the event")
    amount: float = Field(..., description="Amount involved")
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentSummary(BaseModel):
    total_amount: float = Field(..., description="Total transaction amount")
    platform_fee: float = Field(..., description="Platform fee")
    delivery_fee: float = Field(..., description="Delivery service fee")
    store_amount: float = Field(..., description="Amount to be paid to store")
    tax_amount: float = Field(..., description="Tax amount")
    
    @classmethod
    def calculate(cls, subtotal: float, delivery_fee: float, tax_rate: float = 0.08, platform_fee_rate: float = 0.05):
        """Calculate payment distribution"""
        tax_amount = subtotal * tax_rate
        platform_fee = subtotal * platform_fee_rate
        total_amount = subtotal + delivery_fee + tax_amount
        store_amount = subtotal - platform_fee
        
        return cls(
            total_amount=total_amount,
            platform_fee=platform_fee,
            delivery_fee=delivery_fee,
            store_amount=store_amount,
            tax_amount=tax_amount
        ) 