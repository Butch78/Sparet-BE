from typing import List

from fastapi import APIRouter, Depends, Query
from app import deps
from sqlmodel import Session

from app.models import User, UserRead, UserCreate

router = APIRouter()


#  Post user
@router.post("", response_model=UserRead)
async def create_user(
    *, session: Session = Depends(deps.get_session), user: UserCreate
):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(deps.get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> List[UserRead]:
    users = session.query(User).offset(offset).limit(limit).all()
    return users
