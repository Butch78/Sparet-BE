from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from .user import User
from datetime import datetime


# Create a Transaction class that inherits from SQLModel
class TransactionBase(SQLModel):
    name: str
    amount: float 
    category: str
    # date: Optional[datetime] = Field(datetime.now())
    date: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


# Create a Transaction class that inherits from SQLModel
class Transaction(TransactionBase, table=True):
    # Create the fields
    id: int = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="transactions")

# Create a TransactionCreate class that inherits from TransactionBase
class TransactionCreate(TransactionBase):
    pass

# Create a TransactionRead class that inherits from TransactionBase
class TransactionRead(TransactionBase):
    id: int