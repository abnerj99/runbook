from fastapi import HTTPException
import httpx
from sqlalchemy.orm import Session

from app.db.crud import create_job_run, get_job_by_ids, get_one_project_job, update_job_run_failed, update_job_run_success
from app.db.models import Job, JobRun, JobStatus
from app.dramatiq.tasks import execute_job

# Step 2/5 of JobRun Sequence.
def start_job_run(db: Session, job_id: int, user_id: int):
    user_job = get_job_by_ids(db=db, user_id=user_id, job_id=job_id)
    if not user_job: # Caught by 
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )
    
    new_job_run = create_job_run( # insert DB row.
        db=db,
        job_id=job_id,
        status=JobStatus.RUNNING
    )
    # enqueue job.
    execute_job.send(job_id=job_id, job_run_id = new_job_run.id)

    return new_job_run
