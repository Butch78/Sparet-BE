from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from app.models.user import User

# Create a Transaction class that inherits from SQLModel
class TransactionBase(SQLModel):
    name: str
    amount: float
    category: str
    # date: Optional[datetime] = Field(datetime.now())
    date: str
    user_id: int | None = Field(default=None, foreign_key="user.id")


# Create a Transaction class that inherits from SQLModel
class Transaction(TransactionBase, table=True):
    # Create the fields
    id: int = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="transactions")


# Create a TransactionCreate class that inherits from TransactionBase
class TransactionCreate(TransactionBase):
    pass


# Create a TransactionRead class that inherits from TransactionBase
class TransactionRead(TransactionBase):
    id: int
