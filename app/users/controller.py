from app.database.mysqlConnection import Dbsession #db mysql connection created
from . import model
from . import service
from fastapi import FastAPI, APIRouter, status

#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/users', 
    tags=['user']
    )
#get all users at once
@router.get('/allUsers', response_model=list[model.UserResponse])
async def getAllUsers(db:Dbsession):
    return service.getAllUsers(db)

#create new record
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createUser(user:model.UserCreate, db:Dbsession):
    db_user = service.createUser(user,db)
    return {"message":"User created successfully!","response":db_user};

#update user record
@router.put("/{user_id}", response_model=model.UserResponse)
async def updateUser(db:Dbsession, user_id:int, user_update:model.UserBase):
    return service.updateUser(db,user_id,user_update)
    
@router.get("/{user_id}", response_model=model.UserById)
async def getUserById(db:Dbsession, user_id:int):
    return service.getUserById(db,user_id)