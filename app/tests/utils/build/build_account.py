#  Models

from app.models.account import Account, AccountCreate, AccountUpdate, Accounts
from app.models.balance import Balance, BalanceCreate

from app.tests.utils.build.base import BUILDBase

from app.tests.utils import build

#  Model Factory
from pydantic_factories import ModelFactory


class BUILDAccount(BUILDBase[Account, AccountCreate, AccountUpdate]):
    def build_object(self) -> Account:
        object_Factory = ModelFactory.create_factory(
            self.model, account_id="EbLbndnlx4SZpgP3aB49SVWGNgE38qfXvl3LW"
        )
        account = object_Factory.build()
        account.balances.append(build.balance.build_object())
        account.transactions.extend(build.transaction.build_object(size=5))

        return account


account = BUILDAccount(Account, AccountCreate, AccountUpdate)
