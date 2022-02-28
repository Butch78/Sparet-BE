from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class RequestEnum(Enum):
    GET = "GET"
    POST = "POST"


class RequestBase(BaseModel):
    client_id: str = Field(..., title="Client Id")
    secret: str = Field(..., title="Secret")
    access_token: Optional[str] = Field(..., title="Access Token")


class RequestOption(BaseModel):
    count: int = Field(100, title="Count")
    offset: int = Field(0, title="Offset")
    include_original_description: bool = Field(
        True, title="Include Original Description"
    )


class TransactionRequest(RequestBase):
    start_date: str = Field(..., title="Start Date")
    end_date: str = Field(..., title="End Date")
    options: RequestOption = Field(..., title="Options")


class TokenOptions(BaseModel):
    webhook: str = Field(..., title="Webhook")


class TokenRequest(RequestBase):
    institution_id: str = Field(..., title="Institution Id")
    initial_products: List[str] = Field(..., title="Initial Products")
    options: TokenOptions = Field(..., title="Options")


class PaymentMeta(BaseModel):
    by_order_of: str = Field(None, title="By Order Of")
    payee: str = Field(None, title="Payee")
    payer: str = Field(None, title="Payer")
    payment_method: str = Field(None, title="Payment Method")
    payment_processor: str = Field(None, title="Payment Processor")
    ppd_id: str = Field(None, title="PPD ID")
    reason: str = Field(None, title="Reason")
    reference_number: str = Field(None, title="Reference Number")


# Plaid API Models
class Transaction(BaseModel):
    account_id: str = Field(..., title="account_id")
    account_owner: str | None = Field(..., title="account_owner")
    amount: int = Field(..., title="amount")
    iso_currency_code: str = Field(..., title="iso_currency_code")
    name: str = Field(..., title="name")
    payment_meta: PaymentMeta | None = Field(..., title="payment_meta")
    pending: bool = Field(..., title="pending")
    pending_transaction_id: str | None = Field(..., title="pending_transaction_id")
    transaction_id: str = Field(..., title="transaction_id")
    transaction_type: str = Field(..., title="transaction_type")


# List of Transactions
class Transactions(BaseModel):
    transactions: list[Transaction] | None = Field(None, title="transactions")
