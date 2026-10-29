from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy import select
from app.schemas import *
from app.services.auth_services import get_current_user
from app.db.models import *
from app.db.session import Session, get_db
from app.db.crud import *
from app.schemas.jobs import *
from app.services.job_runs import start_job_run
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
        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )
        
        new_job = create_project_job(
            db= db,
            project_id=project_id,
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
def get_project_jobs(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    jobs = get_all_project_jobs(
        db=db,
        user_id=user.id,
        project_id=project_id
    )
    return jobs

@router.get("/project/{project_id}/jobs/{job_id}")
def get_project_job(project_id: int, job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = get_one_project_job(db=db, user_id=user.id, project_id=project_id, job_id=job_id)
    return job


# JobRun.... Hey There.
#---------------
# Step 1/5 of JobRun - Endpoint.
@router.post("/jobs/{job_id}/run", response_model=JobRunResponse)
def post_job_run(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    
    new_job = start_job_run(db = db, job_id = job_id, user_id= user.id)

    return new_job

