from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session
from app.utils.deps import get_session

from app.models.user import User, UserCreate, UserUpdate, UserRead
from app import crud

router = APIRouter()


#  Post user
@router.post("", response_model=User)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    return crud.user.create(db=session, obj_in=user)


#  Read Users
@router.get("", response_model=list[User])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> list[User]:
    return crud.user.get_multi(db=session, skip=offset, limit=limit)


#  Read User
@router.get("/{id}", response_model=User)
def read_user(
    *,
    session: Session = Depends(get_session),
    id: int,
) -> User:
    return crud.user.get(db=session, id=id)


# Update User
@router.patch("/{id}", response_model=User)
def update_user(
    *, session: Session = Depends(get_session), id: Any, user: UserUpdate
) -> User:
    # return crud.user.update(db=session, id=id, obj_in=user)


    db_user = session.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# User Delete
@router.delete("/{id}", response_model=User)
def delete_user(
    *,
    session: Session = Depends(get_session),
    id: int,
) -> User:
    return crud.user.delete(db=session, id=id)
