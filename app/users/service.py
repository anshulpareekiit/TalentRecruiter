from app.database.mysqlConnection import Dbsession
from . import model
from fastapi import FastAPI, status, HTTPException
from app.entities.user import User
from fastapi.responses import JSONResponse
from app.utils.commonFxn import CommonFxn
import base64
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

class UsersService:
    not_found_msg = "Record Not Found!"
    went_wrong_msg = "Something Went Wrong!"
    duplicate_rec = "Email Id or Username already exists!"
    commonObj = CommonFxn()
    
    #CREATE New User
    def createUser(self,user:model.UserCreate, db:Dbsession):
        try:
            duplicate_resp = self._duplicateUser(db, user)
            if duplicate_resp != None:
                 resp = duplicate_resp
            else:
                db_user = User(**user.model_dump())
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                result = {"id":db_user.id}
                resp = JSONResponse(
                    content=result, 
                    status_code=status.HTTP_200_OK
                    )
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{self.went_wrong_msg}:{str(e)}"
                )
    #send password link and set token expiry with token to be checked
    def sendPwdLink(self,db:Dbsession, user_model:model.SendPwdLink):
        user_data = db.query(User).filter(User.username == user_model.username).first()
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        try:
            user_data.password_token = base64.b64encode(user_data.email.encode('utf-8'))
            #self._sendPwdSetEmail(user_data.email, user_data.password_token)
            self._sendPwdSetEmail(user_data)
            self._setToken(user_model, user_data, db)
            return JSONResponse(
                    content={'message':'Password Set Email sent successfully!'}, 
                    status_code=status.HTTP_200_OK
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"{self.went_wrong_msg}:{str(e)}")
        
    
    #setting the token for password reset functionality
    def _setToken(self,user_model:model.SendPwdLink, user_data:User, db:Dbsession):
        now = datetime.now()
        user_data.token_expire_datetime = now + timedelta(minutes = 10)
        user_data.is_token_used = False
        db.commit()
        db.refresh(user_data)
        return user_data
    
    #SEND EMAIL TO SET PASSWORD
    def _sendPwdSetEmail(self,user_data:User):
        subject = "Set Your Password"
        
        body = f"Hi,\n\nClick the link below to set your password:{user_data.password_token}\n\n\nThis link will expire in 30 minutes."
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = "7f7596cfca-fa3cbc+1@inbox.mailtrap.io"
        msg['To'] = user_data.email
        settings.SMTP_HOST
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
        
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())

    #get all user list
    def getAllUsers(self, db:Dbsession):
        #check if record not found then send message
        user = db.query(User.f_name).first()
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
            return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
        except Exception as e:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{self.went_wrong_msg}:{str(e)}")

    #update user details
    def updateUser(self, db: Dbsession, user_id: int, user_data: model.UserUpdate):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            # Safely update only provided fields        
            user_data_dict = user_data.model_dump(exclude_unset=True)
            for key, value in user_data_dict.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)

            resp = {"records Updated": {"id": user.id}}
            return JSONResponse(content=resp, status_code=status.HTTP_200_OK)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Something Went Wrong! {str(e)}"
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
    
    #return response false if duplicate not found else send json reponse for duplicate
    def _duplicateUser(self, db:Dbsession, user:User):
        if db.query(User).filter(
                User.username==user.username,
                User.email == user.email,
            ).first() != None:
            resp = JSONResponse(
                content= self.duplicate_rec, 
                status_code=status.HTTP_204_NO_CONTENT
            )
        else:
            resp = None
        return resp
