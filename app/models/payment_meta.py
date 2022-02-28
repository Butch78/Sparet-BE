from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class PaymentMetaBase(SQLModel):
    by_order_of: str | None = Field(..., title="By Order Of")
    payee: str | None = Field(..., title="Payee")
    payer: str | None = Field(..., title="Payer")
    payment_method: str | None = Field(..., title="Payment Method")
    payment_processor: str | None = Field(..., title="Payment Processor")
    ppd_id: str | None = Field(..., title="PPD ID")
    reason: str | None = Field(..., title="Reason")
    reference_number: str | None = Field(..., title="Reference Number")

    class Config:
        orm_mode = True


class PaymentMeta(PaymentMetaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    transaction_id: int = Field(
        default=None, title="Transaction Id", foreign_key="transaction.transaction_id"
    )
    transaction: Optional["Transaction"] = Relationship(back_populates="payment_meta")


class PaymentMetaCreate(PaymentMetaBase):
    pass


class PaymentMetaUpdate(PaymentMetaBase):
    pass
