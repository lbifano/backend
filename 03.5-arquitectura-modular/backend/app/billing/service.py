"""Service Invoice (negocio) — esqueleto."""

from app.billing.schemas import Invoice, InvoiceCreate
from app.billing.repository import InvoiceRepository


class InvoiceService:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    def list_invoices(self) -> list[Invoice]:
        return self.repository.list_all()

    def create_invoice(self, body: InvoiceCreate) -> Invoice:
        return self.repository.create(body.concept.strip(), body.amount, body.project_id)
