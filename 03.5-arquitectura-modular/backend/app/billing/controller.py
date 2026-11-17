"""Controller Invoice (HTTP) — esqueleto."""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.shared.db import get_session
from app.billing.schemas import InvoiceCreate, InvoiceRead
from app.billing.repository import InvoiceRepository
from app.billing.service import InvoiceService

router = APIRouter(prefix="/api/invoices", tags=["billing"])


def get_invoice_service(session: Session = Depends(get_session)) -> InvoiceService:
    return InvoiceService(InvoiceRepository(session))


@router.get("", response_model=list[InvoiceRead])
def list_invoices(service: InvoiceService = Depends(get_invoice_service)):
    return service.list_invoices()


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(body: InvoiceCreate, service: InvoiceService = Depends(get_invoice_service)):
    return service.create_invoice(body)
