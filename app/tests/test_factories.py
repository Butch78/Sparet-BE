from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Any, Dict, List, Union
from pydantic_factories import ModelFactory


class Species(str, Enum):
    CAT = "Cat"
    DOG = "Dog"


class Pet(BaseModel):
    name: str
    species: Species


class Person(BaseModel):
    id: UUID4
    name: str
    hobbies: List[str]
    age: Union[float, int]
    birthday: Union[datetime, date]
    pets: List[Pet]
    assets: List[Dict[str, Dict[str, Any]]]


def test_factory():

    class PersonFactory(ModelFactory):
        __model__ = Person

    person = PersonFactory.build()


    assert person.pets != []
