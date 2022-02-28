from pickletools import uint4
from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import List, TYPE_CHECKING, Optional


from uuid import uuid4

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.payment_meta import PaymentMeta
    from app.models.location import Location


# Create a Transaction class that inherits from SQLModel
class TransactionBase(SQLModel):
    account_owner: Optional[str] = Field(..., title="Account Owner")
    name: Optional[str] = Field(
        ...,
        title="Name",
    )
    authorized_date: Optional[date] = Field(..., title="Authorized Date")
    authorized_datetime: Optional[date] = Field(..., title="Authorized DateTime")
    category: str = Field(..., title="Category")
    category_id: str = Field(..., title="Category Id")
    check_number: Optional[str] = Field(..., title="Check Number")
    transaction_date: Optional[date] = Field(default_factory=date.today, title="Date")
    transaction_datetime: Optional[date] = Field(
        default_factory=date.today, title="DateTime"
    )
    iso_currency_code: str = Field(..., title="ISO Currency Code")

    # Location

    merchant_name: Optional[str] = Field(..., title="Merchant Name")
    payment_channel: str = Field(..., title="Payment Channel")

    # Payment Meta

    pending: bool = Field(..., title="Pending")
    pending_transaction_id: Optional[str] = Field(..., title="Pending Transaction Id")
    personal_finance_category: Optional[str] = Field(
        ..., title="Personal Finance Category"
    )
    transaction_code: Optional[str] = Field(..., title="Transaction Code")

    transaction_type: str = Field(..., title="Transaction Type")
    unofficial_currency_code: Optional[str] = Field(
        ..., title="Unofficial Currency Code"
    )

    @validator("authorized_date", pre=True)
    def validate_authorized_date(cls, v):
        if v is None:
            return date.today()
        return v

    @validator("authorized_datetime", pre=True)
    def validate_authorized_datetime(cls, v):
        if v is None:
            return date.today()
        return v

    @validator("transaction_date", pre=True)
    def validate_date(cls, v):
        if v is None:
            return date.today()
        return v

    @validator("transaction_datetime", pre=True)
    def validate_datetime(cls, v):
        if v is None:
            return date.today()
        return v

    class Config:
        orm_mode = True


# Create a Transaction class that inherits from SQLModel
class Transaction(TransactionBase, table=True):

    transaction_id: str = Field(
        default_factory=uuid4, title="Transaction Id", primary_key=True
    )

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
