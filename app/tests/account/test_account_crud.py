from sqlmodel import Session
from app import crud
from app.tests.utils import build


from app.tests.utils.conftest import session_fixture, client_fixture


def test_create_account(session: Session):
    test_account = build.account.build_object()
    account = crud.account.create(db=session, obj_in=test_account)
    assert account.mask == test_account.mask
    assert account.name == test_account.name
    assert account.official_name == test_account.official_name
    assert account.subtype == test_account.subtype
    assert account.type == test_account.type
    assert account.account_id is not None
