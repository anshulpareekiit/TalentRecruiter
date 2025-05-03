from app.database.mysqlConnection import Dbsession #db mysql connection created
from . import usersModel
from fastapi import APIRouter, status
from app.api.v1.users.usersService import UsersService
#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/v1/users', 
    tags=['user']
    )

#creating object of User Service
userServiceObj = UsersService()

#####################get all users at once####################
@router.get('/', response_model=list[usersModel.UserResponse])
async def getAllUsers(db:Dbsession, skip: int = 0, limit: int = 10):
    print("ADSFASDFADSF")
    return userServiceObj.getUsers(db, skip=skip, limit=limit)

#####################create new record####################
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createUser(user:usersModel.UserCreate, db:Dbsession):
    return userServiceObj.createUser(user,db)

#####################update user record####################
@router.put("/update/{user_id}", response_model=usersModel.UserUpdate)
async def updateUser(db:Dbsession, user_id:int, user_update:usersModel.UserUpdate):
    return userServiceObj.updateUser(db,user_id,user_update)
    
#####################get record by Id####################
@router.get("/{user_id}", response_model=usersModel.UserById)
async def getUserById(db:Dbsession, user_id:int):
    return userServiceObj.getUserById(db,user_id)

################send password link to user email####################
@router.put("/sendPwdLink")
async def sendPwdLink(db:Dbsession, input_data:usersModel.SendPwdLink):
    return userServiceObj.sendPwdLink(db,input_data)

###############SET PASSWORD####################
@router.put("/setPassword")
def setPassword(db:Dbsession, input_data:usersModel.SetPassword):
    return userServiceObj.setPassword(db,input_data)