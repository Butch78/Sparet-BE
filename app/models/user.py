from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship  

from app import models

# Create a new Person class that inherits from SQLModel
class UserBase(SQLModel):
    name: str
    age: str
    email: str

# Inherit from UserBase
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["User"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass