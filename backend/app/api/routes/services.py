
from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from backend.app.schemas.user import UserCreate, UserRead
from app.services.auth_services import register_user
from app.db.models import *
from app.db.session import Session, get_db
from runbook import router


