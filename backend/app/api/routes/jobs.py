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
from app.db.crud import create_job_run, create_project_job, create_user_project, get_all_project_jobs, get_all_user_projects, get_one_project_job, get_user_project
from app.schemas.user import UserRead
from app.schemas.jobs import *
# Endpoints, Job + JobRun!
router = APIRouter()

@router.post("/project/{project_id}/jobs", response_model=JobResponse)
def post_project_job(project_id: int, data: JobCreate ,db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        project = get_user_project(
            requested_id=project_id,
            user_id=user.id,
            db=db
        )
        
        new_job = create_project_job(
            db= db,
            project_id=data.project_id,
            name = data.name,
            http_method=data.http_method,
            url=str(data.url),
            timeout_seconds=data.timeout_seconds
        )
        db.commit()
        db.refresh(new_job)
        return new_job
    except HTTPException:
        db.rollback()
        raise
        
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create job."
        )
    
@router.get("/project/{project_id}/jobs", response_model=list[JobResponse])
def get_project_jobs(project_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):

    jobs = get_all_project_jobs(
        db=db,
        user_id=user.id,
        project_id=project_id
    )
    return jobs

@router.get("/project/{project_id}/jobs/{job_id}")
def get_project_job(project_id: int, job_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    job = get_one_project_job(db=db, user_id=user.id, project_id=project_id, job_id=job_id)
    return job


# JobRun.... Hey There.
#---------------
@router.post("/jobs/{job_id}/run", response_model=JobRunResponse)
def post_job_run(job_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized."
        )
    new_job_run = create_job_run(db = db, job_id=job_id, status="RUNNING")

    return new_job_run

