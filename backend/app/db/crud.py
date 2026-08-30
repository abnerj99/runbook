

import email

from pytest import Session
from sqlalchemy import select
from app.schemas.user import UserRead
from .models import *
from app.db import models

def create_user(db: Session, name: str, email: str, password_hash: str ) -> User:
    new_user = models.User(
        name=name,
        email=email,
        password_hash = password_hash
    )
    db.add(new_user)
    db.flush()
    return new_user

def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)
    return user

def get_user_by_id(db: Session, user_id: int):
    stmt = select(User).where(User.id == int(user_id))
    user = db.scalar(stmt)
    return user