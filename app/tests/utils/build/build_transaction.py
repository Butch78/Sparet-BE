from app.tests.utils.build.base import BUILDBase


#  Model Factory
from pydantic_factories import ModelFactory


from uuid import uuid4
from sqlmodel import Session
from app.tests.utils import build

# Models

from app.models.transaction import (
    Transaction,
    TransactionCreate,
    TransactionUpdate,
)
from app.models.payment_meta import PaymentMeta, PaymentMetaCreate, PaymentMetaUpdate
from app.models.location import Location, LocationCreate, LocationUpdate


class BUILDTransaction(BUILDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def build_object(self, size: int = 1) -> Transaction | list[Transaction]:
        object_Factory = ModelFactory.create_factory(
            self.model, account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW"
        )
        if size == 1:
            transaction = object_Factory.build()
            transaction.payment_meta.append(build.payment_meta.build_object())
            transaction.location.append(build.location.build_object())
            return transaction

        for _ in range(size):
            transaction = object_Factory.build()
            transaction.payment_meta.append(build.payment_meta.build_object())
            transaction.location.append(build.location.build_object())
            self.objects.append(transaction)

        return self.objects

    def build_create_object(
        self, size: int = 1
    ) -> TransactionCreate | list[TransactionCreate]:
        object_Factory = ModelFactory.create_factory(
            self.create_model, account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW"
        )

        if size == 1:
            transaction = object_Factory.build()
            transaction.payment_meta.append(build.payment_meta.build_create_object())
            transaction.location.append(build.location.build_create_object())
            return transaction

        for _ in range(size):
            transaction = object_Factory.build()
            transaction.payment_meta.append(build.payment_meta.build_create_object())
            transaction.location.append(build.location.build_create_object())
            self.objects.append(transaction)
        return self.objects

    def build_update_object(
        self, size: int = 1
    ) -> TransactionUpdate | list[TransactionUpdate]:
        object_Factory = ModelFactory.create_factory(
            self.update_model, account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW"
        )

        if size == 1:
            transaction = object_Factory.build()
            transaction.payment_meta = build.payment_meta.build_update_object()
            transaction.location = build.location.build_update_object()
            return transaction

        return object_Factory.build()


transaction = BUILDTransaction(Transaction, TransactionCreate, TransactionUpdate)
