from pyexpat import model
from typing import Any, Generic, List, Optional, TypeVar, Union


from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel
from sqlmodel import Session
from fastapi import HTTPException


from app.models.account import Account, AccountCreate, AccountUpdate

from app.crud.base import CRUDBase


class CRUDAccount(CRUDBase[Account, AccountCreate, AccountUpdate]):

    # Id = Account_id on Account model

    def create_multiple(self, db: Session, *, obj_in: List[Account]) -> List[Account]:
        try:
            db_models = []
            for item in obj_in:
                account = self.create(db=db, obj_in=item)
                db_models.append(account)
            return db_models
        except Exception as e:
            print(f"{self.model.__name__} not created")
            print(e)

    def create(self, db: Session, obj_in: AccountCreate) -> Optional[Account]:
        try:
            db_model = self.model.construct(**obj_in.dict())
            db.add(db_model)
            db.commit()
            db.refresh(db_model)
            return db_model
        except Exception as e:
            print(f"{self.model.type.__name__} not created")
            print(e)

    def get(self, db: Session, id: Any) -> Optional[SQLModel]:
        try:
            return db.query(self.model).filter(self.model.account_id == id).first()
        except Exception as e:
            print(f"{self.model.__name__} with the {id} id not found")

    def delete(self, db: Session, *, id: Any) -> Optional[SQLModel]:
        try:
            db_obj = db.query(self.model).filter(self.model.account_id == id).first()
            if db_obj is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.model.__name__} not found"
                )
            db.delete(db_obj)
            db.commit()
            return db_obj
        except Exception as e:
            print(f"{self.model.__name__} not deleted")
            print(e)


account = CRUDAccount(Account)
