from optparse import Option
from typing import List, TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseConfig, BaseModel


# Create a new Person class that inherits from SQLModel
class UserBase(SQLModel):
    name: str = Field(..., title="Name", description="The name of the user")
    age: int = Field(..., title="Age", description="The age of the user")
    email: str = Field(..., title="Email", description="The email of the user")

    class Config:
        anystr_strip_whitespace = True


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
