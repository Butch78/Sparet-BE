from typing import List, TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship

import uuid


class AccountBase(SQLModel):
    mask: Optional[str] = Field(None, title="Mask")
    name: Optional[str] = Field(None, title="Name")
    official_name: Optional[str] = Field(None, title="Official Name")
    subtype: str = Field(None, title="Subtype")
    type: str = Field(None, title="Type")


class Account(AccountBase, table=True):
    account_id: str = Field(str(uuid.uuid4()), primary_key=True)


class AccountCreate(AccountBase):
    pass


class AccountUpdate(SQLModel):
    mask: Optional[str] = None
    name: Optional[str] = None
    official_name: Optional[str] = None
    subtype: Optional[str] = None
    type: Optional[str] = None


class Accounts(SQLModel):
    accounts: List[Account]
    total_transactions: int = Field(..., title="Total Transactions")
    request_id: str = Field(..., title="Request ID")


# # Test Pydantic Models


def test_account_model():

    # Test Account Model
    account = Account(
        account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW",
        name="test_name",
        subtype="test_subtype",
        type="test_type",
    )

    assert account is not None
    assert account.account_id == "EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW"
    print("Hello World")
