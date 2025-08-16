from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from app.core.config import settings
#load_dotenv()

#DBURL = os.getenv("MYSQLURL")

engine = create_engine(settings.MYSQLURL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Commented as per new version of sqlalchemy.orm using class based approach
#Base = declarative_base()#or class Base(declarativeBase


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Dbsession = Annotated[Session, Depends(get_db)]