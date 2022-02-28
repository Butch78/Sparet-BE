
from app.crud.base import CRUDBase
from app.crud.crud_account import account


from app.models.user import User, UserCreate, UserUpdate
from app.models.account import Account, AccountCreate, AccountUpdate
from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.models.balance import Balance, BalanceCreate, BalanceUpdate
from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.payment_meta import PaymentMeta, PaymentMetaCreate, PaymentMetaUpdate


user = CRUDBase[User, UserCreate, UserUpdate](User)
balance = CRUDBase[Balance, BalanceCreate, BalanceUpdate](Balance)
transaction = CRUDBase[Transaction, TransactionCreate, TransactionUpdate](Transaction)
item_account = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
payment_meta = CRUDBase[PaymentMeta, PaymentMetaCreate, PaymentMetaUpdate](PaymentMeta)
account = account
