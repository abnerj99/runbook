
from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.db.schemas import *
from app.services.auth_services import confirm_user, register_user
from app.db.models import *
from app.db.session import Session, get_db

router = APIRouter()

@router.post("/auth/register", response_model=UserRead)
def create_new_user(data: UserCreate, db: Session = Depends(get_db)):
    return register_user(data, db)
    
@router.post("/auth/login", response_model=TokenResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    return confirm_user(data, db)