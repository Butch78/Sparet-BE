# Connet to the Plaid API and get the access token using asyncio.

from fastapi import Depends
from app.services.plaid.models import Transaction
import aiohttp

from app.utils.config import settings


# Plaid Client using the plaid-python package and the Plaid API
class PlaidClient:
    def __init__(self):
        self.base_url = "https://sandbox.plaid.com"
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
                    url="https://sandbox.plaid.com/sandbox/public_token/create",
                    json={
                        "client_id": settings.PLAID_CLIENT_ID,
                        "secret": settings.PLAID_SECRET,
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
                            "client_id": settings.PLAID_CLIENT_ID,
                            "secret": settings.PLAID_SECRET,
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
        self, start_date: str = "2021-01-01", end_data: str = "2021-12-01"
    ) -> list[Transaction]:
        # Get the transactions using the Plaid API

        if self.access_token is None:
            await self.access_token()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=self.base_url + "/transactions/get",
                    json={
                        "client_id": settings.PLAID_CLIENT_ID,
                        "secret": settings.PLAID_SECRET,
                        "access_token": self.access_token,
                        "start_date": start_date,
                        "end_date": end_data,
                    },
                ) as response:
                    response_json = await response.json()
                    print(response_json)
                    return response_json["transactions"]

        except Exception as e:
            print(e)
