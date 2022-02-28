from app.tests.utils import build

from app.models.payment_meta import PaymentMeta, PaymentMetaCreate, PaymentMetaUpdate

from sqlmodel import Session

from app.tests.utils.conftest import session_fixture, client_fixture


def test_create_payment_meta(session: Session):

    test_payment_meta = build.payment_meta.build_object()
    test_payment_create = build.payment_meta.build_create_object()
    test_payment_update = build.payment_meta.build_update_object()

    payment_meta = PaymentMeta(**test_payment_meta.dict())

    session.add(payment_meta)
    session.commit()
    session.refresh(payment_meta)
    assert payment_meta.payee == test_payment_meta.payee
    assert payment_meta.payment_method == test_payment_meta.payment_method
    assert payment_meta.id is not None

    assert test_payment_create is not None
    assert test_payment_update is not None
