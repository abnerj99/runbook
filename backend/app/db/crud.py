

import email

from pytest import Session
from sqlalchemy import select
from app.schemas.user import UserRead
from .models import *
from app.db import models


# Users
#--------------

def create_user(db: Session, name: str, email: str, password_hash: str ) -> User:
    new_user = models.User(
        name=name,
        email=email,
        password_hash = password_hash
    )
    db.add(new_user)
    db.flush()
    return new_user

def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)
    return user

def get_user_by_id(db: Session, user_id: int):
    stmt = select(User).where(User.id == int(user_id))
    user = db.scalar(stmt)
    return user

# Projects
#--------------

def create_user_project(db: Session, user_id: int, name: str, description: str | None):
    new_project = models.Project(
        owner_id = user_id,
        name=name,
        description=description
    )
    db.add(new_project)
    db.flush()
    return new_project

def get_all_user_projects(db: Session, user_id:int):
    stmt = select(Project).where(Project.owner_id == user_id)
    projects = db.scalars(stmt).all()

    return projects

def get_user_project(requested_id: int,user_id: int, db: Session):
    # User owns project, project.id matches requested_id
    stmt = select(Project).where(Project.owner_id == user_id, Project.id == requested_id)
    project = db.scalar(stmt)

    return project

# Jobs
#--------------
def create_project_job(db: Session, 
                       project_id: int, name: str, 
                       http_method: str, url: str, timeout_seconds: int):

    new_job = models.Job(
        project_id = project_id,
        name = name,
        http_method=http_method,
        url=url,
        timeout_seconds=timeout_seconds
    )
    db.add(new_job)
    db.flush()

    return new_job

def get_project_job(db: Session, user_id: int, 
                    project_id: int, job_id: int):
    stmt = select(Job).where(Project.id == project_id, Job.id == job_id, Project.owner_id == user_id)
    job = db.scalar(stmt)

    return job

def get_all_project_jobs(db: Session, user_id: int,
                         project_id: int):
    stmt = select(Project.jobs).where(Project.id == project_id, Project.owner_id == user_id)
    jobs = db.scalars(stmt).all()

    return jobs
