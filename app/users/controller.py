from app.database.mysqlConnection import Dbsession #db mysql connection created
from . import model
from . import service
from fastapi import FastAPI, APIRouter, status
from app.users.service import UsersService
#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/users', 
    tags=['user']
    )
#creating object of User Service
userServiceObj = UsersService()

#get all users at once
@router.get('/allUsers', response_model=list[model.UserResponse])
async def getAllUsers(db:Dbsession, skip: int = 0, limit: int = 10,):
    return userServiceObj.getAllUsers(db, skip=skip, limit=limit)

#create new record
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createUser(user:model.UserCreate, db:Dbsession):
    return userServiceObj.createUser(user,db)

#update user record
@router.put("updateUser/{user_id}", response_model=model.UserResponse)
async def updateUser(db:Dbsession, user_id:int, user_update:model.UserBase):
    return userServiceObj.updateUser(db,user_id,user_update)
    
#get record by Id
@router.get("/{user_id}", response_model=model.UserById)
async def getUserById(db:Dbsession, user_id:int):
    return userServiceObj.getUserById(db,user_id)

@router.put("/sendPwdLink")
async def sendPwdLink(db:Dbsession, input_data:model.SendPwdLink):
    return userServiceObj.sendPwdLink(db,input_data)

@router.put("/setPassword")
def setPassword(db:Dbsession, input_data:model.SetPassword):
    return userServiceObj.setPassword(db,input_data)