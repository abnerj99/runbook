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
    project_id: int
    http_method: HTTPMethod
    url: HttpUrl
    timeout_seconds: int
    enabled: bool
    created_at: datetime
