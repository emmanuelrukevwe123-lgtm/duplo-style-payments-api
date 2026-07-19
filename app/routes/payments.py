from fastapi import APIRouter, HTTPException

from app.metrics import invoices_paid_total
from app.models import Transaction
from app.store import AlreadyPaidError, NotFoundError, store

router = APIRouter(tags=["payments"])


@router.post("/invoices/{invoice_id}/pay", response_model=Transaction)
def pay_invoice(invoice_id: str) -> Transaction:
    try:
        transaction = store.pay_invoice(invoice_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Invoice not found") from None
    except AlreadyPaidError:
        raise HTTPException(status_code=409, detail="Invoice already paid") from None
    invoices_paid_total.inc()
    return transaction


@router.get("/transactions", response_model=list[Transaction])
def list_transactions() -> list[Transaction]:
    return store.list_transactions()
