from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.crud import *
from app.db.models import Job, JobRun, JobStatus
from app.dramatiq.tasks import execute_job

# Step 2/5 of JobRun Sequence. -> Next CRUD / DB 
def start_job_run(db: Session, job_id: int, user_id: int):
    user_job = get_job_by_ids(db=db, user_id=user_id, job_id=job_id)
    if not user_job: # Caught by 
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )
    
    new_job_run = create_job_run( 
        db=db,
        job_id=job_id,
        status=JobStatus.RUNNING
    )
    # enqueue job, not executed immediately.
    execute_job.send(job_id=job_id, job_run_id = new_job_run.id)

    return new_job_run
