"""Modelo Invoice (ORM + schemas) — esqueleto de la feature billing."""

from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class InvoiceBase(SQLModel):
    concept: str = Field(min_length=1, max_length=200)
    amount: float = Field(gt=0)
    project_id: int | None = Field(default=None)


class Invoice(InvoiceBase, table=True):
    __tablename__ = "invoices"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceRead(InvoiceBase):
    id: int
    created_at: datetime
