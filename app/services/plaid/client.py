from typing import List
from fastapi import Depends
from pydantic import parse_obj_as

from sqlmodel import Session
import aiohttp
import json


# Utils
from app import crud
from app.utils.config import settings, Settings

#  Models

from app.models.account import Account, Accounts, AccountwithBalance
from app.models.transaction import Transaction
from app.models.balance import Balance
from app.models.item import Item


# # Plaid-python specific imports
import plaid
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from app.services.plaid.models import (
    TransactionRequest,
    TokenRequest,
    RequestOption,
    RequestEnum,
)

# Plaid Client using the plaid-python package and the Plaid API
class PlaidClient:
    """
    Plaid Client that will be used to retrieve transactions, accounts, and balances.

    """

    def __init__(self, settings: Settings = settings):
        self.base_url = settings.PLAID_URL
        self.PLAID_CLIENT_ID = settings.PLAID_CLIENT_ID
        self.PLAID_SECRET = settings.PLAID_SECRET
        self.access_token: str = None
        self.public_token: str = None

    def format_error(e):
        response = json.loads(e.body)
        return {
            "error": {
                "status_code": e.status,
                "display_message": response["error_message"],
                "error_code": response["error_code"],
                "error_type": response["error_type"],
            }
        }

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

        except plaid.ApiException as e:
            error_response = self.format_error(e)
            print(error_response)
            return error_response

    async def get_access_token(self) -> str:
        # Get the access token using the Plaid API

        if self.public_token is None:
            await self.get_public_token()

        print("Getting access token")

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

        except plaid.ApiException as e:
            error_response = self.format_error(e)
            print(error_response)
            return error_response

    async def plaid_request(self, url, json=None, type: RequestEnum = "GET"):
        """
        Create a request using the Plaid API

        """

        try:

            if type == "GET":
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response_json = await response.json()
                        return response_json

            elif type == "POST":
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=json) as response:
                        response_json = await response.json()
                        return response_json

        except plaid.ApiException as e:
            error_response = self.format_error(e)
            print(error_response)

    async def get_transactions(
        self,
        db: Session,
        start_date: str = "2021-01-01",
        end_date: str = "2021-12-01",
    ) -> Accounts:
        # Get the transactions using the Plaid API

        if self.access_token is None:
            await self.access_token()

        url = self.base_url + "/transactions/get"

        try:
            transaction_request = TransactionRequest(
                client_id=self.PLAID_CLIENT_ID,
                secret=self.PLAID_SECRET,
                access_token=self.access_token,
                start_date=start_date,
                end_date=end_date,
                options=RequestOption(),
            )

            response = await self.plaid_request(
                url=url,
                json=transaction_request.dict(),
                type="POST",
            )

            balances = []

            transactions = response["transactions"]

            accounts = Accounts(
                accounts=parse_obj_as(List[Account], response["accounts"]),
                total_transactions=response["total_transactions"],
                request_id=response["request_id"],
                transactions=None,
                item=Item(**response["item"]),
            )

            db_accounts = crud.account.create_multiple(
                db=db, obj_list=accounts.accounts
            )

            for item in response["accounts"]:
                balances.append(
                    Balance(**item["balances"], account_id=item["account_id"])
                )


            # # add_balances = crud.balance.create_multiple(db=db, obj_in=balances)
            # add_item = crud.item_account.create(db=db, obj_in=accounts.item)

            # add_balances = []

            # # Add each add_balance item to each add_account item
            # for balance in add_balances:
            #     for account in add_accounts:
            #         if account is not None and balance is not None:
            #             if account.account_id == balance.account_id:
            #                 account.balances = balance

            # accounts.accounts = add_accounts
            # accounts.item = add_item

            while len(transactions) < response["total_transactions"]:
                transaction_request.options.offset += len(transactions)
                response = await self.plaid_request(
                    url=url, json=transaction_request.dict(), type="POST"
                )
                transactions += response["transactions"]

            # json to pydanitc list
            # add_transactions = crud.transaction.create_multiple(
            #     db=db, obj_in=
            # )

            # accounts.transactions = add_transactions

            return accounts

        except plaid.ApiException as e:
            error_response = self.format_error(e)
            print(error_response)

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

        except plaid.ApiException as e:
            error_response = self.format_error(e)
            print(error_response)
            return error_response
