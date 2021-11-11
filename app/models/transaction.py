from typing import Optional
from sqlmodel import Field, SQLModel


# Create a Transaction class that inherits from SQLModel
class Transaction(SQLModel, table=True):
    # Create the fields
    id: int = Field(int, primary_key=True, auto_increment=True)
    name: str = Field(str, nullable=True)
    person_id: int = Field(int, nullable=False)
    amount: float = Field(float, nullable=False)
    category: str = Field(str, nullable=False)
    date: str = Field(str, nullable=False)

    # Create a class method to get all transactions
    @classmethod
    def get_all_transactions(cls, session: Session) -> Optional[list]:
        """
        Get all transactions from the database.
        :param session: The current database session.
        :return: A list of transactions or None if no transactions are found.
        """
        return cls.select(session)

    # Create a class method to get a transaction by ID
    @classmethod
    def get_transaction_by_id(cls, session: Session, id: int) -> Optional[list]:
        """
        Get a transaction by ID from the database.
        :param session: The current database session.
        :param id: The ID of the transaction.
        :return: A list of transactions or None if no transactions are found.
        """
        return cls.select(session, where=f"id = {id}")

    # Create a class method to get a transaction by name
    @classmethod
    def get_transaction_by_name(cls, session: Session, name: str) -> Optional[list]:
        """
        Get a transaction by name from the database.
        :param session: The current database session.
        :param name: The name of the transaction.
        :return: A list of transactions or None if no transactions are found.
        """
        return cls.select(session, where=f"name = '{name}'")

    # Create a class method to get a transaction by amount
    @classmethod
    def get_transaction_by_amount(cls, session: Session, amount: float) -> Optional[list]:
        """
        Get a transaction by amount from the database.
        :param session: The current database session.
        :param amount: The amount of the transaction.
        :return: A list of transactions or None if no transactions are found.
        """
        return cls.select(session, where=f"amount = {amount}")

    #  Create a class method to get a transaction by invest ID
    @classmethod
    def get_transaction_by_invest_id(cls, session: Session, person_id: int) -> Optional[list]:
        """
        Get a transaction by person ID from the database.
        :param session: The current database session.
        :param person_id: The person ID of the transaction.
        :return: A list of transactions or None if no transactions are found.
        """
        return cls.select(session, where=f"invest_id = {invest_id}")