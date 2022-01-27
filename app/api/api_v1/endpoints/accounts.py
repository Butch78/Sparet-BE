from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session
from app.utils.deps import get_session

from app.models.account import Account, AccountCreate, AccountUpdate, AccountwithBalance
from app import crud

router = APIRouter()


#  Post account
@router.post("", response_model=Account)
def create_account(
    *, session: Session = Depends(get_session), account: Account
) -> Account:
    return crud.account.create(db=session, obj_in=account)


#  Get Accounts
@router.get("", response_model=list[AccountwithBalance])
def read_accounts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> list[Account]:
    return crud.account.get_multi(db=session, skip=offset, limit=limit)


#  Get Account
@router.get("/{account_id}", response_model=Account)
def read_account(
    *,
    session: Session = Depends(get_session),
    account_id: Any,
) -> Account:
    return crud.account.get(db=session, id=account_id)


#  Update Account
@router.patch("/{account_id}", response_model=Account)
def update_account(
    *,
    session: Session = Depends(get_session),
    account_id: Any,
    account: AccountUpdate,
) -> Account:
    return crud.account.update(db=session, id=account_id, obj_in=account)


#  Delete Account
@router.delete("/{account_id}", response_model=Account)
def delete_account(
    *,
    session: Session = Depends(get_session),
    account_id: Any,
) -> Account:
    return crud.account.delete(db=session, id=account_id)
