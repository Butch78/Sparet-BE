# Connet to the Plaid API and get the access token using asyncio.

from cmath import acos
from fastapi import Depends
from app.models.account import Accounts
from app.models.transaction import Transaction
from app.models.balance import Balance
from app.models.item import Item
from app import crud
from sqlmodel import Session
import aiohttp
import asyncer

from app.utils.config import settings, Settings


# Plaid Client using the plaid-python package and the Plaid API
class PlaidClient:
    def __init__(self, settings: Settings = settings):
        self.base_url = settings.PLAID_URL
        self.PLAID_CLIENT_ID = settings.PLAID_CLIENT_ID
        self.PLAID_SECRET = settings.PLAID_SECRET
        self.access_token: str = None
        self.public_token: str = None

    async def create_request(self, url, json=None):
        """
        Create a request using the Plaid API

        """
        return self.oauth2_session.post(url, json=json)

    async def oauthentic_client(self):

        # 1. Call Link Token Creation
        # 3. Call Public Token Exchange for Access Token
        # 3. Store Access Token

        # TODO implement better error handling
        # TODO retrieve link token from database

        try:
            if self.access_token is None:
                print("Initializing Plaid Client")
                await self.get_access_token()
        except Exception as e:
            print(e)

    async def get_public_token(self) -> str:
        """
        Get the link token using the Plaid API

        """
        print("Getting public token")

        try:

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.base_url + "/sandbox/public_token/create",
                    json={
                        "client_id": self.PLAID_CLIENT_ID,
                        "secret": self.PLAID_SECRET,
                        "institution_id": "ins_3",
                        "initial_products": ["auth", "transactions"],
                        "options": {
                            "webhook": "https://www.genericwebhookurl.com/webhook"
                        },
                    },
                ) as response:
                    response_json = await response.json()
                    print(response_json)
                    self.public_token = response_json["public_token"]
                    return self.public_token

        except Exception as e:
            print(e)

    async def get_access_token(self) -> str:
        # Get the access token using the Plaid API

        print("Getting access token")

        if self.public_token is None:
            await self.get_public_token()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.base_url + "/item/public_token/exchange",
                    json={
                        "client_id": self.PLAID_CLIENT_ID,
                        "secret": self.PLAID_SECRET,
                        "public_token": self.public_token,
                    },
                ) as response:
                    response_json = await response.json()
                    print(response_json)
                    self.access_token = response_json["access_token"]
                    return self.access_token

        except Exception as e:
            print(e)

    async def get_transactions(
        self,
        db: Session,
        start_date: str = "2021-01-01",
        end_data: str = "2021-12-01",
    ) -> Accounts:
        # Get the transactions using the Plaid API

        if self.access_token is None:
            await self.access_token()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.base_url + "/transactions/get",
                    json={
                        "client_id": self.PLAID_CLIENT_ID,
                        "secret": self.PLAID_SECRET,
                        "access_token": self.access_token,
                        "start_date": start_date,
                        "end_date": end_data,
                    },
                ) as response:
                    response_json = await response.json()

                    accounts = Accounts(**response_json)

                    balances = []

                    for item in response_json["accounts"]:
                        balances.append(
                            Balance(**item["balances"], account_id=item["account_id"])
                        )

                    item_obj = Item(**response_json["item"])

                    try:

                        add_accounts = crud.account.create_multiple(
                            db=db, obj_in=accounts.accounts
                        )

                        add_balances = crud.balance.create_multiple(
                            db=db, obj_in=balances
                        )

                        add_item = crud.item_account.create(db=db, obj_in=item_obj)

                        # Add each add_balance item to each add_account item
                        for balance in add_balances:
                            for account in add_accounts:
                                if account is not None and balance is not None:
                                    if account.account_id == balance.account_id:
                                        account.balances.append(balance)

                        accounts.accounts = add_accounts

                        return accounts

                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)

    async def get_accounts(self, session: Session) -> Accounts:
        # Get the accounts using the Plaid API

        if self.access_token is None:
            await self.access_token()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.base_url + "/accounts/balance/get",
                    json={
                        "client_id": self.PLAID_CLIENT_ID,
                        "secret": self.PLAID_SECRET,
                        "access_token": self.access_token,
                    },
                ) as response:
                    response_json = await response.json()

                    accounts = Accounts(**response_json)
                    print(accounts)

                    return accounts

        except Exception as e:
            print(e)


    
