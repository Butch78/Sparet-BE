from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
import json
from app import crud


from app.tests.utils.conftest import session_fixture, client_fixture

from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate


from app.tests.utils import build


def test_create_transaction(session: Session):

    test_transaction = build.transaction.build_object()

    transaction = test_transaction

    transaction = crud.transaction.create(db=session, obj_in=transaction)

    assert transaction.authorized_date == test_transaction.authorized_date
    assert transaction.transaction_id == test_transaction.transaction_id
    assert transaction.account_id == test_transaction.account_id
    assert transaction.transaction_type == test_transaction.transaction_type
    assert transaction.transaction_code == test_transaction.transaction_code

    assert transaction.location is not None
    assert transaction.transaction_id is not None
