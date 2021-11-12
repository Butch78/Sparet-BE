from typing import Optional
from sqlmodel import Field, SQLModel


# Create a Transaction class that inherits from SQLModel
class TransactionBase(SQLModel):
    name: str
    amount: float 
    category: str
    date: str 
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


# Create a Transaction class that inherits from SQLModel
class Transaction(TransactionBase, table=True):
    # Create the fields
    id: int = Field(int, primary_key=True)

# Create a TransactionCreate class that inherits from TransactionBase
class TransactionCreate(TransactionBase):
    pass

# Create a TransactionRead class that inherits from TransactionBase
class TransactionRead(TransactionBase):
    id: int