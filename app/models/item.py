from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional
from datetime import datetime

from pydantic import ValidationError, validator

if TYPE_CHECKING:
    from app.models.account import Account


class ItemBase(SQLModel):
    available_products: str = Field(..., title="Available Products")
    billed_products: str = Field(..., title="Billed Products")
    consent_expiration_time: str = Field(
        default_factory=datetime.utcnow, title="Consent Expiration Time"
    )
    error: str = Field(..., title="Error")
    institution_id: str = Field(..., title="Institution Id")
    item_id: str = Field(..., title="Item Id")
    products: str = Field(..., title="Products")
    update_type: str = Field(..., title="Update Type")
    webhook: str = Field(..., title="Webhook")

    @validator("available_products", pre=True)
    def validate_available_products(cls, v):
        if v is None:
            return "assets, balance"
        return v

    @validator("billed_products", pre=True)
    def validate_billed_products(cls, v):
        if v is None:
            return "auth, transactions"
        return v

    @validator("consent_expiration_time", pre=True)
    def validate_consent_expiration_time(cls, v):
        if v is None:
            return str(datetime.utcnow())
        return v

    @validator("error", pre=True)
    def validate_error(cls, v):
        if v is None:
            return "No Error!"
        return v

    @validator("products", pre=True)
    def validate_products(cls, v, values):
        if v is None:
            return values["billed_products"]
        return v

    @validator("update_type", pre=True)
    def validate_update_type(cls, v):
        if v is None:
            return "background"
        return v

    @validator("webhook", pre=True)
    def validate_webhook(cls, v):
        if v is None:
            return "https://www.genericwebhookurl.com/webhoo"
        return v


class Item(ItemBase, table=True):
    item_id: str = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass
