from cgi import test
from statistics import mode
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


from app.utils.deps import get_session
from app.main import app
from app.models.user import User, UserUpdate


from pydantic_factories import ModelFactory


class UserFactory(ModelFactory):
    __model__ = User


class UserUpdateFactory(ModelFactory):
    __model__ = UserUpdate


test_user = UserFactory.build()


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


def test_get_all_users_with_no_users(session: Session, client: TestClient):
    response = client.get("/users")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


def test_create_user(client: TestClient):

    test_user = UserFactory.build()

    response = client.post("/users", json=test_user.dict())
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == test_user.name
    assert data["age"] == test_user.age
    assert data["email"] == test_user.email
    assert data["id"] is not None


def test_create_user_incomplete(client: TestClient):
    # No secret_name
    response = client.post("/users", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_user_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/users",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_users(session: Session, client: TestClient):
    user_1 = UserFactory.build()
    user_2 = UserFactory.build()
    session.add(user_1)
    session.add(user_2)
    session.commit()

    response = client.get("/users")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == user_1.name
    assert data[0]["age"] == user_1.age
    assert data[0]["email"] == user_1.email
    assert data[0]["id"] is not None
    assert data[1]["name"] == user_2.name
    assert data[1]["age"] == user_2.age
    assert data[1]["email"] == user_2.email
    assert data[1]["id"] is not None


def test_read_user(session: Session, client: TestClient):
    user = UserFactory.build()
    session.add(user)
    session.commit()

    response = client.get(f"/users/{user.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == user.name
    assert data["age"] == user.age
    assert data["email"] == user.email
    assert data["id"] == user.id


def test_update_user(session: Session, client: TestClient):
    user = UserFactory.build()
    session.add(user)
    session.commit()

    response = client.patch(
        f"/users/{user.id}",
        json={"name": "Deadpuddle", "age": "100", "email": "hello@hotmail.com"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["age"] == 100
    assert data["email"] == "hello@hotmail.com"
    assert data["id"] == user.id


def test_delete_user(session: Session, client: TestClient):
    user = UserFactory.build()
    session.add(user)
    session.commit()

    response = client.delete(f"/users/{user.id}")

    user_in_db = session.get(User, user.id)

    assert response.status_code == 200

    assert user_in_db is None
