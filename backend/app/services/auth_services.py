import stat
from fastapi import Depends, HTTPException
from pytest import Session

from app.db.crud import create_user, get_user_by_email, get_user_by_id
from app.schemas.user import UserCreate, UserLogin
from app.db.session import get_db
from app.services.errors import InvalidCredentialsError
from app.services.token import create_access_token, verify_access_token
from .security import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


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

def verify_credentials(data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)

    if user is None:
        raise InvalidCredentialsError()
    
    try:
        verify_password(user.password_hash, data.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return create_access_token(user.id)

def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
    ):
    payload = verify_access_token(token)
    user_id = payload["sub"]
    
    return get_user_by_id(db, user_id)
