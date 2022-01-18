import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


from app.utils.deps import get_session
from app.main import app
from app.models.account import Account, AccountCreate, AccountUpdate
from app.models.item import Item


from pydantic_factories import ModelFactory


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class AccountCreateFactory(ModelFactory):
    __model__ = Account


test_account = AccountCreateFactory.build()


def test_get_all_accounts_with_no_accounts(session: Session, client: TestClient):
    response = client.get("/accounts")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


def test_create_account(client: TestClient):

    test_account = AccountCreateFactory.build()

    response = client.post("/accounts", json=test_account)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_account.name
    assert data["balance"] == test_account.balance
    assert data["currency"] == test_account.currency
    assert data["id"] == test_account.id
