"""
Created By: Anshul Pareek
Modified by: Anshul pareek
Last Modified: 20-Apr-25 
Description: Create database schema once you run the server create the table with columns specified
"""
from sqlalchemy import Boolean, Column, Integer, String
from app.database.mysqlConnection import Base

#creating user table with columns
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    f_name = Column(String(50))
    l_name = Column(String(50))
    email = Column(String(100))
    mobile = Column(String(10))