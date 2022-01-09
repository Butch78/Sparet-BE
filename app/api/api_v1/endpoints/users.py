from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session
from app.utils.deps import get_session

from app.models.user import User, UserRead, UserCreate

router = APIRouter()


#  Post user
@router.post("", response_model=UserRead)
async def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


#  Read Users
@router.get("", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[UserRead]:
    users = session.query(User).offset(offset).limit(limit).all()
    return users
