from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from app import models, deps
from sqlmodel import Session
from app.models.transaction import Transaction, TransactionCreate, TransactionRead



router = APIRouter()


#  Post Transaction
@router.post("", response_model=TransactionRead)
def create_transaction(*, session: Session = Depends(deps.get_session), transaction: TransactionCreate)->TransactionRead:
    db_transaction = Transaction.from_orm(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.get("", response_model=List[TransactionRead])
def read_transactions(
    *,
    session: Session = Depends(deps.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),)->List[TransactionRead]:
    transactions = session.query(Transaction).all()
    return [Transaction.to_orm(transaction) for transaction in transactions]