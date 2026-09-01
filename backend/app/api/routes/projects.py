from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from app.schemas import *
from app.services.auth_services import register_user, verify_credentials, get_current_user
from app.db.models import *
from app.db.session import Session, get_db
from app.services.errors import InvalidCredentialsError
from app.schemas.projects import ProjectCreate, ProjectResponse
from app.db.crud import create_user_project
from app.schemas.user import UserRead

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
def create_project(data: ProjectCreate, db: Session = Depends(get_db),user = Depends(get_current_user)):
        try:
            new_project = create_user_project(
            db=db,
            user_id=user.id,
            name=data.name,
            description=data.description
        )
            db.commit()
            db.refresh(new_project)
            return new_project
        except:
            db.rollback()
            raise HTTPException(
                 status_code=500,
                 detail="Failed to create project."
            )

@router.get("/projects", response_model=ProjectResponse)
def get_projects(user = Depends(get_current_user), db: Session = Depends(get_db)):
    pass
    