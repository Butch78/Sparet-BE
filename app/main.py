from fastapi import FastAPI

app = FastAPI()

from app.utils.deps import create_db_and_tables
from app.api.api_v1.api import api_router
from app.utils.config import settings

app.include_router(api_router)


@app.on_event("startup")
async def on_startup():
    print(settings.PLAID_CLIENT_ID)
    create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    pass
