
from fastapi import APIRouter, Depends, HTTPException
from typing import List

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items",
    tags=["items"],
    # TODO: Add dependencies
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


from app.models import Transaction


# Create Fastapi Transactions endpoints
@router.get("/", response_model=List[Transaction])
async def get_transactions(db_session):
    return db_session.query(Transaction).all()


# Create Fastapi Transaction by id endpoints
@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(db_session, transaction_id):
    return db_session.query(Transaction).filter(Transaction.id == transaction_id).first()
