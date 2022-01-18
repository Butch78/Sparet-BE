from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.payment_meta import PaymentMeta
    from app.models.location import Location


# Create a Transaction class that inherits from SQLModel
class TransactionBase(SQLModel):
    account_owner: str = Field(..., title="Account Owner")
    name: str = Field(
        ...,
        title="Name",
    )

    authorized_date: datetime | None = Field(..., title="Authorized Date")
    authorized_datetime: datetime | None = Field(..., title="Authorized DateTime")
    category: list[str] = Field(..., title="Category")
    category_id: str = Field(..., title="Category Id")
    check_number: str | None = Field(..., title="Check Number")
    date: datetime | None = Field(..., title="Date")
    iso_currency_code: str = Field(..., title="ISO Currency Code")

    # Location

    merchant_name: str = Field(..., title="Merchant Name")
    name: str = Field(..., title="Name")
    payment_channel: str = Field(..., title="Payment Channel")

    # Payment Meta

    pending: bool = Field(..., title="Pending")
    pending_transaction_id: str | None = Field(..., title="Pending Transaction Id")
    personal_finance_category: str | None = Field(
        ..., title="Personal Finance Category"
    )
    transaction_code: str | None = Field(..., title="Transaction Code")

    transaction_type: str = Field(..., title="Transaction Type")
    unofficial_currency_code: str | None = Field(..., title="Unofficial Currency Code")


# Create a Transaction class that inherits from SQLModel
class Transaction(TransactionBase, table=True):

    transaction_id: str = Field(default=None, title="Transaction Id", primary_key=True)

    account_id: str = Field(
        default=None, title="Account Id", foreign_key="account.account_id"
    )

    #  Relationships
    account: Optional["Account"] = Relationship(back_populates="transactions")
    location: Optional["Location"] = Relationship(back_populates="transaction")
    payment_meta: Optional["PaymentMeta"] = Relationship(back_populates="transaction")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass
