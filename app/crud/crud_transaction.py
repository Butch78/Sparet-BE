from pyexpat import model
from typing import Any, Generic, List, Optional, TypeVar, Union


from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel
from sqlmodel import Session
from fastapi import HTTPException


from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate

from app.crud.base import CRUDBase


class CRUDTransaction([Transaction, TransactionCreate, TransactionUpdate]):
    pass
