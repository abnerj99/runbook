from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.user import UserRead
from .db.database import Base, engine
from .db.session import get_db, Session
from sqlalchemy import select
from .db.models import *
from .api.routes import runbook, projects, jobs

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(runbook.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "Ok"}

@app.get("/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users

