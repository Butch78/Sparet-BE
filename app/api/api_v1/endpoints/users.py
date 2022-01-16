from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session
from app.utils.deps import get_session

from app.models.user import User, UserCreate, UserUpdate

router = APIRouter()


#  Post user
@router.post("", response_model=User)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    db_user = User.from_orm(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


#  Read Users
@router.get("", response_model=list[User])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
) -> list[User]:
    users = session.query(User).offset(offset).limit(limit).all()
    return users


#  Read User
@router.get("/{user_id}", response_model=User)
def read_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> User:
    user = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update User
@router.patch("/{user_id}", response_model=User)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user: UserUpdate,
) -> User:
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# User Delete
@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
) -> User:
    db_user = session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return db_user
