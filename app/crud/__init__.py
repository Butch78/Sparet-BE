# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)

# custom crud from .crud_user import user


from app.crud.base import CRUDBase


from app.models.user import User, UserCreate, UserUpdate
from app.models.account import Account, AccountCreate, AccountUpdate
from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.models.balance import Balance, BalanceCreate, BalanceUpdate
from app.models.item import Item, ItemCreate, ItemUpdate
from app.models.payment_meta import PaymentMeta, PaymentMetaCreate, PaymentMetaUpdate


user = CRUDBase[User, UserCreate, UserUpdate](User)
account = CRUDBase[Account, AccountCreate, AccountUpdate](Account)

# from app.crud.crud_account import account
