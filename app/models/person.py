from typing import Optional
from sqlmodel import Field, SQLModel


# Create a new Person class that inherits from SQLModel
class Person(SQLModel, table=True):
    id = Field(int, primary_key=True)
    name = Field(str)
    age = Field(int)
    email = Field(str)

    