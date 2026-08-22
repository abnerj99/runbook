from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Base, engine
from .db.session import get_db, Session
from sqlalchemy import select
from .db.models import *


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "Ok"}

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()

    return users

@app.post("/users")
def create_user(name: str, db: Session = Depends(get_db)):
    user = User(name=name)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user