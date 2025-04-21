from app.database.mysqlConnection import Dbsession
from . import model
from . import service
from fastapi import FastAPI, status, HTTPException
from app.entities.user import User
from fastapi.responses import JSONResponse
from app.utils.commonFxn import CommonFxn

class UsersService:
    not_found_msg = "Record Not Found!"
    went_wrong_msg = "Something Went Wrong!"
    commonObj = CommonFxn()

    def createUser(self,user:model.UserCreate, db:Dbsession):
        try:
            db_user = User(
                username=user.username,
                f_name=user.f_name, 
                l_name=user.l_name, 
                email=user.email, 
                mobile=user.mobile,
                password=user.password
                )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            resp = {"id":db_user.id}
            return JSONResponse(
                content=resp, 
                status_code=status.HTTP_200_OK
                )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{self.went_wrong_msg}:{str(e)}"
                )
        

    #get all user list
    def getAllUsers(self, db:Dbsession):
        #check if record not found then send message
        user = db.query(User).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=self.not_found_msg)
        try:
            #Fetching users
            users = db.query(
                User.f_name, 
                User.l_name, 
                User.username,
                User.email,
                User.mobile
                ).all()
            #converting in the List
            resp = [model.UserResponse.model_validate(user).model_dump() for user in users]
            return JSONResponse(
                content=resp,
                status_code=status.HTTP_200_OK
                )
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{self.went_wrong_msg}:{str(e)}")

    #update user details
    def updateUser(self,db:Dbsession, user_id:int, user_data:model.UserUpdate):
        try:
            user = db.query(User).filter(User.id==user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, message=self.not_found_msg)
            
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
            resp = {"records Updated":{"id":user.id}}
            return JSONResponse(content=user, status_code=status.HTTP_200_OK)
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{self.went_wrong_msg} str{e}"
                )

    def getUserById(self,db:Dbsession, user_id:int):
        try:
            result = db.query(User).filter(User.id == user_id).first();
            
            if result != None:
                #converting response in json format
                return model.UserById.model_validate(result).model_dump()
            else:
                return HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail=f"{self.went_wrong_msg} : {str(e)}")        
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{self.went_wrong_msg} : {str(e)}")