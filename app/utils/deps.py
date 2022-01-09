from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from app.services.plaid.client import PlaidClient
from functools import lru_cache
from app.utils.config import settings


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


#  Create Client


async def get_plaid_client() -> PlaidClient:
    try:
        client = PlaidClient()
        
        await client.oauthentic_client()
        yield client
    except Exception as e:
        print(e)
