from app.database.mysqlConnection import Dbsession
from . import model
from . import service
from fastapi import FastAPI, APIRouter, status
from app.users.schema import User

def createUser(user:model.UserCreate, db:Dbsession):
    db_user = User(
        f_name=user.f_name, 
        l_name=user.l_name, 
        email=user.email, 
        mobile=user.mobile
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#get all user list
def getAllUsers(db:Dbsession)-> list[User]:
    data = db.query(User).all()
    return data