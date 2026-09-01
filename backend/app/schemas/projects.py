from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str | None

class ProjectResponse(BaseModel):
    name: str
    description: str 
    created_at: datetime
    updated_at: datetime
