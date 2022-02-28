from app.models.balance import Balance, BalanceCreate, BalanceUpdate
from app.tests.utils.build.base import BUILDBase


#  Model Factory
from pydantic_factories import ModelFactory


class BUILDBalance(BUILDBase[Balance, BalanceCreate, BalanceCreate]):
    def build_object(self) -> Balance:
        object_Factory = ModelFactory.create_factory(
            self.model,
            account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW",
        )
        return object_Factory.build()

    def build_create_object(self) -> BalanceCreate:
        object_Factory = ModelFactory.create_factory(
            self.model,
            account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW",
        )
        return object_Factory.build()

    def build_update_object(self) -> BalanceUpdate | list[BalanceUpdate]:
        object_Factory = ModelFactory.create_factory(
            self.model,
            account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW",
        )
        return object_Factory.build()


balance = BUILDBalance(Balance, BalanceCreate, BalanceCreate)
