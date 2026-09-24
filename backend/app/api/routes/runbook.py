
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from app.schemas.user import *
from app.services.auth_services import register_user, verify_credentials, get_current_user
from app.db.models import *
from app.db.session import Session, get_db
from app.services.errors import InvalidCredentialsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter()

@router.post("/auth/register", response_model=UserRead)
def create_new_user(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(data, db)
    
@router.post("/auth/login", response_model=TokenResponse)
def login_user(
    #data: UserLogin, - future
    form_data: OAuth2PasswordRequestForm = Depends(), # Temp - 
    db: Session = Depends(get_db)): # Temp, production testing AUTH.
    try:
        data = UserLogin(
            email=form_data.username,
            password=form_data.password,
        ) # Temp
        token = verify_credentials(data, db)
        
        return TokenResponse(
            access_token=token
        )
    except InvalidCredentialsError:
        raise HTTPException(status_code=401,
                            detail="Invalid email or password.")

@router.get("/users/me", response_model=UserRead)
def get_user(user = Depends(get_current_user)):
    return user




