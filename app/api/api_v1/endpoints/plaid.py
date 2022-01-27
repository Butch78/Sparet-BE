from typing import List
from fastapi import APIRouter, Depends
from app.models.account import Accounts, AccountwithBalance
from app.services.plaid.client import PlaidClient
from app.services.plaid.models import Transaction


from app.utils.deps import get_plaid_client, get_session

from typing import List

# Api Router
router = APIRouter()


@router.get("/")
async def ping():
    return {"message": "pong"}


# Get Transactions from Plaid
@router.get("/transactions", response_model=Accounts)
async def get_transactions(
    *, client: PlaidClient = Depends(get_plaid_client), session=Depends(get_session)
):
    print(client.access_token)
    transactions = await client.get_transactions(db=session)
    print(transactions)
    return transactions
