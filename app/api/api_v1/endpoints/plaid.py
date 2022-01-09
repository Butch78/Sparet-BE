from fastapi import APIRouter, Depends
from app.services.plaid.client import PlaidClient
from app.services.plaid.models import Transaction
from app.utils.deps import get_plaid_client

# Api Router
router = APIRouter()


# Get Transactions from Plaid
@router.get("/transactions", response_model=list[Transaction])
async def get_transactions(*, client: PlaidClient = Depends(get_plaid_client)):
    print(client.access_token)
    transactions = await client.get_transactions()
    print(transactions)
    return transactions
