from pydantic import BaseModel, Field


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
