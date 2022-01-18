from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from app.models.account import Account


class ItemBase(SQLModel):
    available_products: list[str] | None = Field(...)
    billed_products: list[str] | None = Field(...)
    consent_expiration_time: str | None = Field(...)
    error: str | None = Field(...)
    institution_id: str | None = Field(...)
    item_id: str | None = Field(...)
    products: list[str] | None = Field(...)
    update_type: str | None = Field(...)
    webhook: str | None = Field(...)


class Item(ItemBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass
