from typing import List, TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship

from app.models.transaction import Transaction
from app.models.balance import Balance
import uuid
from app.utils.config import settings, Settings
from pydantic import ValidationError, validator
from pydantic.validators import dict_validator


if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.balance import Balance, BalancewithAccount


class AccountBase(SQLModel):
    mask: Optional[str] = Field(None, title="Mask")
    name: Optional[str] = Field(None, title="Name")
    official_name: Optional[str] = Field(None, title="Official Name")
    subtype: str = Field(None, title="Subtype")
    type: str = Field(None, title="Type")

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


class Account(AccountBase, table=True):
    account_id: str = Field(str(uuid.uuid4()), primary_key=True)
    balances: List["Balance"] = Relationship(back_populates="account")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    pass


class AccountUpdate(SQLModel):
    mask: Optional[str] = None
    name: Optional[str] = None
    official_name: Optional[str] = None
    subtype: Optional[str] = None
    type: Optional[str] = None


class AccountRead(AccountBase):
    account_id: str = Field(..., title="Account ID")


class AccountwithBalance(AccountRead):
    balances: List[Balance] = []


class Accounts(SQLModel):
    accounts: List[AccountwithBalance] = Field(..., title="Accounts")
    total_transactions: int = Field(..., title="Total Transactions")
    transactions: Optional[List[Transaction]] = Field(..., title="Transactions")
    request_id: str = Field(..., title="Request ID")
