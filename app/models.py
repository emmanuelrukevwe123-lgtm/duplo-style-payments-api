from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class InvoiceStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"


class InvoiceCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    amount_ngn: float = Field(gt=0)
    due_date: date


class Invoice(InvoiceCreate):
    id: str
    status: InvoiceStatus = InvoiceStatus.PENDING
    created_at: datetime


class Transaction(BaseModel):
    id: str
    invoice_id: str
    amount_ngn: float
    paid_at: datetime
