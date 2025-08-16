"""JD details"""
from sqlalchemy import String, Boolean,DateTime, Time, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import TYPE_CHECKING
from app.entities.base import Base
from app.entities.associationTables import company_users
#importing company with typechecking to prevent circular import
if TYPE_CHECKING:
    from app.entities.user import User
    from app.entities.company import Company

class JobDescription(Base):
    __tablename__ = "jobDescription"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'), nullable=False)
    preferred_location: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    primary_technology:Mapped[str] = mapped_column(String(200), nullable=False)
    Secondary_technology: Mapped[str] = mapped_column(String(200), nullable=False)
    years_of_experience:Mapped[float] = mapped_column(Float, nullable=False)
    relevant_experience: Mapped[float] = mapped_column(Float, nullable=False)
    notice_period:Mapped[float] = mapped_column(Float, nullable=False)
    job_title: Mapped[str | None] = mapped_column(String(100))
    employment_type: Mapped[str] = mapped_column(String(100), default=True)
    remote_option: Mapped[bool] = mapped_column(Boolean, default=False)
    preferred_qualification: Mapped[str] = mapped_column(String(255), default=False)
    required_qualification: Mapped[str] = mapped_column(String(255), default=False)
    
    generated_jd_text: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    
    #ForeignKey Relationship 
    company: Mapped["Company"] = relationship("Company", back_populates="job_descriptions")