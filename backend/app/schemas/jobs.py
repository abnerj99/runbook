from datetime import datetime
from pydantic import BaseModel, HttpUrl
from app.db.models import HTTPMethod

class JobCreate(BaseModel):
    name: str
    http_method: HTTPMethod
    url: HttpUrl
    timeout_seconds: int | None = None

class JobResponse(BaseModel):
    name: str
    id: int
    project_id: int
    http_method: HTTPMethod
    url: HttpUrl
    timeout_seconds: int
    enabled: bool
    created_at: datetime

class JobRunResponse(BaseModel):
    job_id: int
    status: str
    started_at: datetime 
    finished_at: datetime | None
    status_code: int | None
    duration_ms: int | None
    error_message: str | None
    created_at: datetime