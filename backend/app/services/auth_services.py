import stat
from fastapi import Depends, HTTPException
from pytest import Session

from app.db.crud import create_user, get_user_by_email
from app.db.schemas import UserCreate, UserLogin
from app.db.session import get_db
from app.services.errors import InvalidCredentialsError
from .security import *

def register_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(data.password)
        new_user = create_user(db,
                            name=data.name,
                            email=data.email,
                            password_hash=hashed_password
                            )
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception:
        db.rollback()
        raise

def confirm_user(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)

    if user is None:
        raise InvalidCredentialsError()
    
    try:
        verify_password(user.password_hash, data.password)
        return {"status": verify_password} # Add Refresh Token Return.
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
