from typing import Optional
from sqlmodel import Field, SQLModel


class Investment(SQLModel, table=True):
    id = Field(int, primary_key=True, auto_increment=True)
    name = Field(str, max_length=100, nullable=False)
    description = Field(str, max_length=500, nullable=False)
    amount = Field(int, nullable=False)
    date = Field(str, nullable=False)
    user_id = Field(int, nullable=False)