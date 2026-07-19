"""In-memory data store.

Kept behind this small interface so it can be swapped for a real
database (e.g. Postgres) without touching the route handlers.
"""

import uuid
from datetime import UTC, datetime

from app.models import Invoice, InvoiceCreate, InvoiceStatus, Transaction


class AlreadyPaidError(Exception):
    pass


class NotFoundError(Exception):
    pass


class InMemoryStore:
    def __init__(self) -> None:
        self._invoices: dict[str, Invoice] = {}
        self._transactions: list[Transaction] = []

    def create_invoice(self, data: InvoiceCreate) -> Invoice:
        invoice = Invoice(
            id=str(uuid.uuid4()),
            created_at=datetime.now(UTC),
            **data.model_dump(),
        )
        self._invoices[invoice.id] = invoice
        return invoice

    def list_invoices(self) -> list[Invoice]:
        return list(self._invoices.values())

    def get_invoice(self, invoice_id: str) -> Invoice:
        try:
            return self._invoices[invoice_id]
        except KeyError:
            raise NotFoundError(invoice_id) from None

    def pay_invoice(self, invoice_id: str) -> Transaction:
        invoice = self.get_invoice(invoice_id)
        if invoice.status is InvoiceStatus.PAID:
            raise AlreadyPaidError(invoice_id)
        invoice.status = InvoiceStatus.PAID
        transaction = Transaction(
            id=str(uuid.uuid4()),
            invoice_id=invoice.id,
            amount_ngn=invoice.amount_ngn,
            paid_at=datetime.now(UTC),
        )
        self._transactions.append(transaction)
        return transaction

    def list_transactions(self) -> list[Transaction]:
        return list(self._transactions)

    def reset(self) -> None:
        self._invoices.clear()
        self._transactions.clear()


store = InMemoryStore()
