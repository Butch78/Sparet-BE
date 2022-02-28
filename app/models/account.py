from typing import List, TYPE_CHECKING, Optional
from pytest import Item
from sqlmodel import Field, SQLModel, Relationship

from app.models.transaction import Transaction, TransactionCreate
from app.models.balance import Balance, BalanceCreate
import uuid
from pydantic import ValidationError, validator
from pydantic.validators import dict_validator
from app.models.item import Item


if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.balance import Balance


class AccountBase(SQLModel):
    mask: Optional[str] = Field(None, title="Mask")
    name: Optional[str] = Field(None, title="Name")
    official_name: Optional[str] = Field(None, title="Official Name")
    subtype: Optional[str] = Field(None, title="Subtype")
    type: Optional[str] = Field(None, title="Type")

    @validator("mask", pre=True)
    def validate_mask(cls, v):
        if v is None:
            return "0000"
        return v

    @validator("name", pre=True)
    def validate_name(cls, v):
        if v is None:
            return "Account"
        return v

    # If offical name is not provided, use name instead if it is provided
    @validator("official_name", pre=True)
    def validate_official_name(cls, v, values):
        if v is None:
            v = values.get("name")
        return v

    @validator("subtype", pre=True)
    def validate_subtype(cls, v):
        if v is None:
            return "Account"
        return v

    class Config:
        orm_mode = True


class Account(AccountBase, table=True):
    account_id: str = Field(str(uuid.uuid4()), primary_key=True)
    balances: List["Balance"] = Relationship(back_populates="account")
    transactions: List["Transaction"] = Relationship(back_populates="account")

    class Config:
        orm_mode = True


class AccountCreate(AccountBase):
    mask: str = Field(None, title="Mask")
    name: str = Field(None, title="Name")
    official_name: str = Field(None, title="Official Name")
    subtype: str = Field(None, title="Subtype")
    type: str = Field(None, title="Type")
    balances: Optional[List[BalanceCreate]] = Field(None, title="Balances")
    transactions: Optional[List[TransactionCreate]] = Field(None, title="Transactions")


class AccountUpdate(AccountBase):
    pass


class AccountRead(AccountBase):
    account_id: str = Field(..., title="Account ID")


class AccountwithBalance(AccountRead):
    balances: Balance = Field(..., title="Balances")


class Accounts(SQLModel):
    accounts: List[Account] = Field(..., title="Accounts")
    total_transactions: int = Field(..., title="Total Transactions")
    transactions: Optional[List[Transaction]] = Field(..., title="Transactions")
    request_id: Optional[str] = Field(..., title="Request ID")
    item: Optional[Item] = Field(..., title="Item")
