import json
from app.models.account import Account, AccountCreate


def test_create_model():

    with open("app/tests/data/account_item.json") as json_file:
        account = json.load(json_file)

    account_model = AccountCreate(**account)

    assert account_model.balances is not None


def test_account_model():
    with open("app/tests/data/account_item.json") as json_file:
        account = json.load(json_file)

    account_model = Account(**account)

    assert account_model.balances is not None
