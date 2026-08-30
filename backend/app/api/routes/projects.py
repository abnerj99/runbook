from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from backend.app.schemas.user import *
from app.services.auth_services import register_user, verify_credentials, get_current_user
from app.db.models import *
from app.db.session import Session, get_db
from app.services.errors import InvalidCredentialsError
from runbook import router

@router.get("/projects",)