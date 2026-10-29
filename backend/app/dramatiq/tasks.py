import time
import dramatiq
import httpx
from app.dramatiq.queue import broker
from app.db.database import SessionLocal
from app.db.models import Job
from app.db.crud import get_job, get_one_job_run, update_job_run_failed, update_job_run_success


class JobExecutionError(Exception):
    def __init__(self, message: str, duration_ms: int):
        super().__init__(message)
        self.duration_ms = duration_ms

#Step 4/5 of JobRun
@dramatiq.actor(max_retries=3)
def execute_job(job_id: int, job_run_id: int):
    db = SessionLocal() # worker db session
    job_run = None
    duration_ms = None

    try:
        job = get_job(db, job_id) 
        job_run = get_one_job_run(db, job_run_id)

        if job is None or job_run is None:
            raise ValueError("Job or JobRun not found.")
        
        print(f'Executing: {job.name}, {job.http_method}, {job.url}')

        result = run_job(job)
        response = result["response"]

        if 200 <= response.status_code < 400:
            update_job_run_success(
            db=db,
            job_run= job_run,
            status_code=response.status_code,
            duration_ms=result["duration_ms"]
        )
        else:
            update_job_run_failed(
                db=db,
                job_run = job_run,
                error=f'HTTP: {response.status_code} : {response.reason_phrase}',
                duration_ms=result["duration_ms"],
                status_code=response.status_code
            )

    except Exception as e:
        if isinstance(e, JobExecutionError):
            duration_ms = e.duration_ms
        if job_run is not None:
            update_job_run_failed(
                db=db,
                job_run = job_run,
                error=str(e),
                duration_ms=duration_ms
            )

        raise 
    finally:
        
        db.close()


# Step 5/5 of JobRun

def run_job(job: Job):
    # Performs HTTP Request with HTTPx
    # Saves Result.

    start = time.perf_counter()

    try:

        response = httpx.request(
            method= job.http_method.value,
            url= job.url,
            timeout= job.timeout_seconds
        )

        duration_ms = round((time.perf_counter() - start) * 1000)

    
        return {
            "response": response,
            "duration_ms": duration_ms
        }
    except httpx.RequestError as e: # Connection level failure
        duration_ms = round((time.perf_counter() - start) * 1000)
        raise JobExecutionError(str(e), duration_ms) from e


   