import dramatiq
import httpx
from sqlalchemy.orm import Session
from app.dramatiq.queue import broker
from app.db.database import SessionLocal
from app.db.models import Job, JobRun, JobStatus
from app.db.crud import get_job, get_one_job_run, update_job_run_failed, update_job_run_success

#Step 3.5/5 of JobRun
@dramatiq.actor
def execute_job(job_id: int, job_run_id: int):
    db = SessionLocal() # worker db session
    job_run = None
    try:
        job = get_job(db, job_id) 
        job_run = get_one_job_run(db, job_run_id)

        if job is None:
            print(f'Job {job_id} not found.')
            return
        
        # Step 4/5 of JobRun
        print(f'Executing: {job.name}, {job.http_method}, {job.url}')

        run_job(db=db, job_id =job_id, job_run_id =job_run_id)


    except Exception as e:
        update_job_run_failed(
            db=db,
            job_run = job_run,
            error=str(e),
        )
    finally:
        
        db.close()


# Step 4/5 of JobRun
def run_job(db: Session, job_id: int, job_run_id: int):
    # Performs HTTP Request with HTTPx
    # Saves Result.
    # try, except.
    job = get_job(db=db, job_id=job_id)
    job_run = get_one_job_run(db = db, job_run_id=job_run_id)
    
     # Step 5/5 of JobRun
    response = httpx.request(
        method= job.http_method.value,
        url= job.url,
        timeout= job.timeout_seconds
    )
    
    update_job_run_success(
        db=db,
        job_run= job_run,
        status_code=response.status_code,

    )
    return response

   