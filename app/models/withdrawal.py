from datetime import datetime
from sqlmodel import Field, SQLModel
from datetime import datetime

# Withdrawal model
class Withdrawal(SQLModel, table=True):
    id: int = Field(int, primary_key=True)
    amount: float
    date: datetime
    status: str
    method: str
    reference: str
    description: str
    created_at: datetime
    updated_at: datetime
    person_id: int | None = Field(default=None, foreign_key="person.id")
