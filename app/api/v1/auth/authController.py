from app.database.mysqlConnection import Dbsession #db mysql connection created
from . import authModel
from fastapi import APIRouter, status
from app.api.v1.auth.authService import AuthService
#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/v1/auth', 
    tags=['auth']
    )

#creating object of User Service
authObj = AuthService()

#####################validate user (Login)####################
@router.post('/login', response_model=authModel.AuthResponse)
async def login(credentials:authModel.AuthicateUser, db:Dbsession):
    return authObj.validateUser(db, credentials)