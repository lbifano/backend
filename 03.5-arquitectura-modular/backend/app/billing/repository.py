"""Repository Invoice (ORM) — esqueleto."""

from sqlmodel import Session, select

from app.billing.schemas import Invoice


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Invoice]:
        return list(self.session.exec(select(Invoice).order_by(Invoice.id)).all())

    def create(self, concept: str, amount: float, project_id: int | None = None) -> Invoice:
        invoice = Invoice(concept=concept, amount=amount, project_id=project_id)
        self.session.add(invoice)
        self.session.commit()
        self.session.refresh(invoice)
        return invoice
