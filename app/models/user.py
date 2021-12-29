from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


# Create a new Person class that inherits from SQLModel
class UserBase(SQLModel):
    name: str = Field(..., title="Name", description="The name of the user")
    age: int = Field(..., title="Age", description="The age of the user")
    email: str = Field(..., title="Email", description="The email of the user")

    class Config:
        anystr_strip_whitespace = True


# Inherit from UserBase
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass
