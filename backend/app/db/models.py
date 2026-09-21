from datetime import datetime
from .database import Base
from enum import Enum
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, null, true, Enum as SQLENum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    projects: Mapped[list["Project"]] = relationship(back_populates="owner")


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(150), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    owner: Mapped["User"] = relationship(back_populates="projects")
    jobs: Mapped[list["Job"]] = relationship(
        back_populates="project"
    )

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    http_method: Mapped[HTTPMethod] = mapped_column(
        SQLENum(HTTPMethod, name="http_method"),
        nullable=False
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    timeout_seconds: Mapped[int] = mapped_column( nullable=False, server_default="30")

    enabled: Mapped[bool] = mapped_column(Boolean, default=True, server_default=true(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    project: Mapped["Project"] = relationship(
        back_populates="jobs"
    )