from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from app import models
from sqlmodel import Session
from app.models.transaction import Transaction, TransactionCreate

from app.services.plaid import client, models as plaid_models
from app.utils import deps


router = APIRouter()

# TODO create plain generator for transactions


#  Post Transaction
@router.post("", response_model=Transaction)
def create_transaction(
    *, session: Session = Depends(deps.get_session), transaction: TransactionCreate
) -> Transaction:
    db_transaction = Transaction.from_orm(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("", response_model=List[Transaction])
def read_transactions(
    *,
    session: Session = Depends(deps.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[Transaction]:
    transactions = session.query(Transaction).all()
    return [Transaction.to_orm(transaction) for transaction in transactions]
