from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional
from app.models.account import Account


class BalanceBase(SQLModel):
    available: float = Field(...)
    current: float = Field(...)
    iso_curreny_code: str = Field(...)
    limit: float | None = Field(...)
    unofficial_currency_code: str | None = Field(...)


class Balance(BalanceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    account_id: Optional[str] = Field(
        default=None, title="Account Id", foreign_key="account.account_id"
    )
    account: Optional[Account] = Relationship(back_populates="balances")


class BalanceCreate(BalanceBase):
    pass


class BalanceUpdate(BalanceBase):
    pass
