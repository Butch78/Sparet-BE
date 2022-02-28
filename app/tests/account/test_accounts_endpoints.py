import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.user import User, UserUpdate

from app.tests.utils import build


from app.tests.utils.conftest import session_fixture, client_fixture
from app.models.account import Account, AccountCreate, AccountUpdate


def test_get_all_accounts_with_no_accounts(session: Session, client: TestClient):
    response = client.get("/accounts")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


def test_create_account(
    client: TestClient,
):

    test_account = build.account.build_object()
    response = client.post("/accounts", json=test_account.dict())
    data = response.json()
    assert response.status_code == 200
    assert data["mask"] == test_account.mask
    assert data["name"] == test_account.name
    assert data["official_name"] == test_account.official_name
    assert data["subtype"] == test_account.subtype
    assert data["type"] == test_account.type
    assert data["account_id"] == test_account.account_id


def test_create_account_endpoint_no_id(client: TestClient):

    test_account = build.account.build_create_object()

    response = client.post("/accounts", json=test_account.dict())
    data = response.json()

    assert response.status_code == 200
    assert data["mask"] == test_account.mask
    assert data["name"] == test_account.name
    assert data["official_name"] == test_account.official_name
    assert data["subtype"] == test_account.subtype
    assert data["type"] == test_account.type
    assert data["account_id"] is not None


def test_get_account(client: TestClient):
    test_account = build.account.build_create_object()
    response = client.post("/accounts", json=test_account.dict())
    data = response.json()
    account_id = data["account_id"]
    response = client.get(f"/accounts/{account_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["mask"] == test_account.mask
    assert data["name"] == test_account.name
    assert data["official_name"] == test_account.official_name
    assert data["subtype"] == test_account.subtype
    assert data["type"] == test_account.type
    assert data["account_id"] is not None


def test_update_account(client: TestClient):
    test_account = build.account.build_create_object()
    response = client.post("/accounts", json=test_account.dict())
    data = response.json()
    account_id = data["account_id"]
    test_account_update = AccountUpdate(official_name="New official name")
    response = client.patch(
        f"/accounts/{account_id}", json=test_account_update.dict(exclude_none=True)
    )
    data = response.json()
    assert response.status_code == 200
    assert data["mask"] == test_account.mask
    assert data["name"] == test_account.name
    assert data["official_name"] == test_account_update.official_name
    assert data["subtype"] == test_account.subtype
    assert data["type"] == test_account.type
    assert data["account_id"] is not None


def test_delete_account(session: Session, client: TestClient):

    account = build.account.build_create_object()
    response = client.post("/accounts", json=account.dict())
    data = response.json()

    account_id = data["account_id"]

    response = client.delete(f"/accounts/{account_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["account_id"] == account_id
