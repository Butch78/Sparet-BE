from fastapi import APIRouter

from app.api.api_v1.endpoints import transactions, users, plaid


api_router = APIRouter()
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(plaid.router, prefix="/plaid", tags=["Plaid"])
