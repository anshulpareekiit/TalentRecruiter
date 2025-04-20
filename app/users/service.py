from app.database.mysqlConnection import Dbsession
from . import model
from . import service
from fastapi import FastAPI, APIRouter, status, HTTPException
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
def getAllUsers(db:Dbsession):
    data = db.query(
        User.f_name, 
        User.l_name, 
        User.username
        ).all()
    return data

def updateUser(db:Dbsession, user_id:int, user_data:model.UserUpdate):
    user = db.query(User).filter(User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404, message="no user found with id!")
    
    if user.f_name:
        user.f_name = user_data.f_name
    if user.l_name:
        user.l_name = user_data.l_name
    if user.username:
        user.username = user_data.username
    if user.email:
        user.email = user_data.email
    if user.mobile:
        user.mobile = user_data.mobile
    db.commit()
    db.refresh(user)
    #db.query(User).filter(User.id == user_id).update(user)
    #db.commit()
    return user

def getUserById(db:Dbsession, user_id:int):
    return db.query(User).filter(User.id == user_id).first();