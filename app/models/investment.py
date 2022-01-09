from sqlmodel import Field, SQLModel
from datetime import datetime


class Investment(SQLModel, table=True):
    id: int = Field(int, primary_key=True)
    name: str
    description: str = str | None
    amount: float
    date: datetime
    person_id: int | None = Field(default=None, foreign_key="person.id")
