from fastapi import APIRouter, HTTPException, status

from app.models import Invoice, InvoiceCreate
from app.store import NotFoundError, store

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("", response_model=Invoice, status_code=status.HTTP_201_CREATED)
def create_invoice(data: InvoiceCreate) -> Invoice:
    return store.create_invoice(data)


@router.get("", response_model=list[Invoice])
def list_invoices() -> list[Invoice]:
    return store.list_invoices()


@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str) -> Invoice:
    try:
        return store.get_invoice(invoice_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Invoice not found") from None
