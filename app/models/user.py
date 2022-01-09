from typing import List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

# TO enire there are not circular dependencies we use TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.transaction import Transaction

# Create a new Person class that inherits from SQLModel
class UserBase(SQLModel):
    name: str = Field(..., title="Name", description="The name of the user")
    age: int = Field(..., title="Age", description="The age of the user")
    email: str = Field(..., title="Email", description="The email of the user")

    class Config:
        anystr_strip_whitespace = True


# Inherit from UserBase
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    pass
