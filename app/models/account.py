from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.balance import Balance


class AccountBase(SQLModel):
    mask: str = Field(..., title="Mask")
    name: str = Field(..., title="Name")
    official_name: str = Field(..., title="Official Name")
    subtype: str = Field(..., title="Subtype")
    type: str = Field(..., title="Type")
    total_transactions: int = Field(..., title="Total Transactions")


class Account(AccountBase, table=True):
    account_id: str = Field(default=None, primary_key=True)
    balances: List["Balance"] = Relationship(back_populates="account")
    transactions: List["Transaction"] = Relationship(back_populates="account")


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass
