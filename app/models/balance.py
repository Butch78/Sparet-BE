
from sqlmodel import Field, SQLModel, Relationship
from typing import List, TYPE_CHECKING, Optional

from uuid import UUID, uuid4

from pydantic import validator


if TYPE_CHECKING:
    from app.models.account import Account, AccountRead


class BalanceBase(SQLModel):
    available: float = Field(default=0.0, title="Available")
    current: float = Field(default=0.0, title="Current")
    iso_curreny_code: str = Field(default="CHF", title="ISO Currency Code")
    limit: float = Field(0.0, title="Limit")
    unofficial_currency_code: str = Field("", title="Unofficial Currency Code")

    @validator("current", pre=True)
    def validate_current(cls, v):
        if v is None:
            return 0.0
        return v

    @validator("available", pre=True)
    def validate_available(cls, v):
        if v is None:
            return 0.0
        return v

    @validator("limit", pre=True)
    def validate_limit(cls, v):
        if v is None:
            return 0.0
        return v

    @validator("iso_curreny_code", pre=True)
    def validate_iso_curreny_code(cls, v):
        if v is None:
            return "CHF"
        return v

    @validator("unofficial_currency_code", pre=True)
    def validate_unofficial_currency_code(cls, v):
        if v is None:
            return "CHF"
        return v

    class Config:
        orm_mode = True


# class BalancewithAccount(BalanceBase):
#     account: Optional[AccountRead] = Field(default=None, title="Account")


class Balance(BalanceBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: Optional[str] = Field(
        default=None, title="Account Id", foreign_key="account.account_id"
    )
    account: Optional["Account"] = Relationship(back_populates="balances")

    class Config:
        orm_mode = True


class BalanceCreate(BalanceBase):
    pass


class BalanceUpdate(BalanceBase):
    pass
