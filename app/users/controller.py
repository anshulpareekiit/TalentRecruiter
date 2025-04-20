from app.database.mysqlConnection import Dbsession #db mysql connection created
from . import model
from . import service
from fastapi import FastAPI, APIRouter, status

#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/users', 
    tags=['user']
    )

@router.get('/allUsers/', response_model=list[model.UserResponse])
async def getAllUsers(db:Dbsession):
    return service.getAllUsers(db)


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createUser(user:model.UserCreate, db:Dbsession):
    try:
        db_user = service.createUser(user,db)
    except Exception as e:
        print("error:::"+e);
        return {'err':e}
    return {"message":"User created successfully!","response":db_user};

    