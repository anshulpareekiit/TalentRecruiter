"""
Created By: Anshul Pareek
Modified by: Anshul pareek
Last Modified: 20-Apr-25 
Description: Create database schema once you run the server create the table with columns specified
"""
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped
#from app.database.mysqlConnection import Base

#As per new version following the sqlalchemy orm
class Base(DeclarativeBase):
    pass

#creating user table with columns
class User(Base):
    __tablename__ = 'users'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(50), unique=True)
    f_name:Mapped[str] = mapped_column(String(50), nullable=False)
    l_name:Mapped[str] = mapped_column(String(50), nullable= False)
    email:Mapped[str] = mapped_column(String(100), nullable= False)
    mobile:Mapped[str] = mapped_column(String(10), nullable=True)
    password:Mapped[str] =mapped_column(String(200), nullable=False)