from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Create a new Person class that inherits from SQLModel
class Investor(SQLModel, table=True):
    id = Field(int, primary_key=True)
    name = Field(str)
    age = Field(int)
    email = Field(str)

    # Create a class method to get all the people
    