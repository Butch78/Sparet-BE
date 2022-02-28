from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import json
from app import crud


from app.tests.utils.conftest import session_fixture, client_fixture

#  Models
from app.models.account import Account, AccountCreate, AccountUpdate, Accounts
from app.models.balance import Balance

from app.tests.utils import build


def test_create_account(session: Session):

    test_account = build.account.build_object()

    account = test_account

    session.add(account)
    session.commit()
    session.refresh(account)
    assert account.mask == test_account.mask
    assert account.name == test_account.name
    assert account.official_name == test_account.official_name
    assert account.subtype == test_account.subtype
    assert account.type == test_account.type
    assert account.account_id is not None


def test_get_accounts(session: Session):

    test_account_1 = build.account.build_object()
    test_account_2 = build.account.build_object()

    account_1 = test_account_1
    account_1.account_id = str(uuid4())

    account_2 = test_account_2
    account_2.account_id = str(uuid4())

    assert account_1.account_id != account_2.account_id

    session.add(account_1)
    session.add(account_2)

    session.commit()

    session.refresh(account_1)
    session.refresh(account_2)

    assert account_1.mask == test_account_1.mask
    assert account_1.name == test_account_1.name
    assert account_1.official_name == test_account_1.official_name
    assert account_1.subtype == test_account_1.subtype
    assert account_1.type == test_account_1.type
    assert account_1.account_id is not None

    assert account_2.mask == test_account_2.mask
    assert account_2.name == test_account_2.name
    assert account_2.official_name == test_account_2.official_name
    assert account_2.subtype == test_account_2.subtype
    assert account_2.type == test_account_2.type
    assert account_2.account_id is not None


def test_create_account_one_to_many(
    session: Session,
    client: TestClient,
):

    test_account = build.account.build_object()

    account = test_account

    session.add(account)
    session.commit()
    session.refresh(account)

    assert account.mask == test_account.mask
    assert account.name == test_account.name
    assert account.official_name == test_account.official_name
    assert account.subtype == test_account.subtype
    assert account.type == test_account.type
    assert account.account_id is not None

    assert account.balances is not None
    assert account.balances[0].account_id == test_account.account_id
    assert account.balances[0].id is not None

    response = client.get(f"/accounts/{account.account_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["account_id"] == account.account_id


def test_create_account_json(session: Session, client: TestClient):
    #  Import Json file

    with open("app/tests/data/account_item.json") as json_file:
        account = json.load(json_file)

    print(account)

    response = client.post("/accounts", json=account)
    data = response.json()
    assert response.status_code == 200
    assert data["account_id"] == response.json()["account_id"]


def test_delete_account(session: Session, client: TestClient):

    account = build.account.build_object()

    session.add(account)
    session.commit()
    session.refresh(account)

    response = client.delete(f"/accounts/{account.account_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["account_id"] == account.account_id


def test_create_multiple(session: Session):

    test_account_1 = build.account.build_create_object()
    test_account_2 = build.account.build_create_object()

    account_1 = Account(**test_account_1.dict())
    account_1.account_id = str(uuid4())

    account_2 = Account(**test_account_2.dict())
    account_2.account_id = str(uuid4())

    accounts = []
    accounts.append(account_1)
    accounts.append(account_2)

    accounts = crud.account.create_multiple(db=session, obj_in=accounts)

    assert accounts is not None
