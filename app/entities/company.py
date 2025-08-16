"""company details"""
from sqlalchemy import String, Boolean,DateTime, Time
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.entities.base import Base
from app.entities.associationTables import company_users
#importing company with typechecking to prevent circular import
if TYPE_CHECKING:
    from app.entities.user import User
    from app.entities.jobDescription import JobDescription

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    start_time:Mapped[Time] = mapped_column(Time, nullable=True)
    end_time: Mapped[Time] = mapped_column(Time, nullable=True)
    email:Mapped[str] = mapped_column(String(50), nullable=False)
    contact: Mapped[str] = mapped_column(String(20), nullable=False)
    location:Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    
    users = relationship("User",secondary=company_users, back_populates="companies")
    # One-to-many relationship
    job_descriptions: Mapped[list["JobDescription"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )    