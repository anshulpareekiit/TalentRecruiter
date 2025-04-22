"""
Created By: Anshul Pareek
Modified by: Anshul pareek
Last Modified: 20-Apr-25 
Description: Create database schema once you run the server create the table with columns specified
"""
from sqlalchemy import Integer, String, Boolean, ForeignKey, Enum as SqlEnum, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from app.entities.base import Base

#importing company with typechecking to prevent circular import
if TYPE_CHECKING:
    from app.entities.company import Company
    
    
class UserRole(str, Enum):
    super_admin = 'super_admin'
    company_user = 'company_user'
    


#creating user table with columns
class User(Base):
    __tablename__ = 'users'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    f_name:Mapped[str] = mapped_column(String(50), nullable=False)
    l_name:Mapped[str] = mapped_column(String(50), nullable= False)
    email:Mapped[str] = mapped_column(String(100), nullable= False)
    mobile:Mapped[str] = mapped_column(String(10), nullable=True)
    role:Mapped[UserRole] = mapped_column(SqlEnum(UserRole), default=UserRole.company_user, nullable=False)
    company_id:Mapped[int|None] = mapped_column(ForeignKey('companies.id'), nullable=True)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    password:Mapped[str] =mapped_column(String(200), nullable=False)
    created_at:Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    #from app.entities.company import Company    
    #company: Mapped["Company"] = relationship("Company", back_populates="users")
    


