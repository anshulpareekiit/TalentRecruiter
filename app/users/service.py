from app.database.mysqlConnection import Dbsession
from . import model
from fastapi import status, HTTPException
from app.entities.user import User
from fastapi.responses import JSONResponse
from app.utils.commonFxn import CommonFxn
import base64
from datetime import datetime, timedelta
from app.labels.userLabels import UserLabels 
from sqlalchemy import or_

class UsersService:
    commonObj = CommonFxn()
    
    #CREATE New User
    def createUser(self,user:model.UserCreate, db:Dbsession):
        try:
            duplicate_resp = self._duplicateUser(db, user)
            if duplicate_resp is not None:
                resp = JSONResponse(
                        content={"message":UserLabels.err_msg_duplicate_rec},
                        status_code=status.HTTP_409_CONFLICT  # 204 means "No Content", but 409 (Conflict) is more appropriate
                        )
                 
            else:
                db_user = User(**user.model_dump())
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                resp = JSONResponse(
                    content={"message":UserLabels.msg_user_created_success}, 
                    status_code=status.HTTP_200_OK
                    )
            return resp
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail={"message":UserLabels.err_msg_went_wrong, 'info':UserLabels.err_detail.format(exception = e)}
                )
            
    #send password link and set token expiry with token to be checked
    def sendPwdLink(self,db:Dbsession, user_model:model.SendPwdLink):
        user_data = db.query(User).filter(User.username == user_model.username).first()
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail={"message":UserLabels.err_msg_record_not_found})
        try:
            user_data.password_token = base64.b64encode(user_data.email.encode('utf-8'))
            self._sendPwdSetEmail(user_data)
            self._setToken(user_data, db)
            return JSONResponse(
                    content=UserLabels.msg_email_sent_successfully, 
                    status_code=status.HTTP_200_OK
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=UserLabels.msg_err_send_email.format(exception=e))
        
    
   
    """################setting up the password for user############"""
    def setPassword(self, db:Dbsession, user_data:model.SetPassword):
        #checking if user has not used token and password token in the request matches with provided by user
        token_active = self._isTokenActive(db,user_data)
        user_exists = self._userExists(db,user_data)
        if token_active and user_exists is not None:
            try:
                # Safely update only provided fields
                user_data.is_token_used = True
                user_data_dict = user_data.model_dump(exclude_unset=True)
                for key, value in user_data_dict.items():
                    setattr(user_exists, key, value)
                db.commit()
                db.refresh(user_exists)
                
                return JSONResponse(content={'message':UserLabels.msg_password_set_success}, 
                                    status_code=status.HTTP_200_OK
                                    )
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                    detail={"message":UserLabels.err_msg_went_wrong, 'info':UserLabels.err_detail.format(exception = e)}
                                    )
        
        
    #get all user list
    def getAllUsers(self, db:Dbsession, skip: int = 0, limit: int = 10):
        #check if record not found then send message
        user = db.query(User.f_name).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=UserLabels.err_msg_record_not_found
                            )
        try:
            #Fetching users
            users = db.query(
                User.f_name, 
                User.l_name, 
                User.username,
                User.email,
                User.mobile
                ).offset(skip).limit(limit).all()
            #converting in the List
            resp = [model.UserResponse.model_validate(user).model_dump() for user in users]
            return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 detail={
                                     "message":UserLabels.err_msg_went_wrong, 
                                     'info':UserLabels.err_detail.format(exception = e)
                                    })

    #update user details
    def updateUser(self, db: Dbsession, user_id: int, user_data: model.UserUpdate):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message':UserLabels.err_msg_record_not_found})
            # Safely update only provided fields        
            user_data_dict = user_data.model_dump(exclude_unset=True)
            for key, value in user_data_dict.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            print(user.username)
            resp = {"message": UserLabels.msg_update_success}
            return JSONResponse(content=resp, status_code=status.HTTP_200_OK)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message":UserLabels.err_msg_went_wrong, 'info':UserLabels.err_detail.format(exception = e)}
                )
            

    def getUserById(self,db:Dbsession, user_id:int):
        try:
            result = db.query(User).filter(User.id == user_id).first();
            
            if result != None:
                #converting response in json format
                resp = model.UserById.model_validate(result).model_dump()
            else:
                raise HTTPException(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                detail={"message":UserLabels.err_msg_record_not_found}
                                )
            return resp
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail={"message":UserLabels.err_msg_went_wrong, 'info':UserLabels.err_detail.format(exception = e)})
    
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

    #Check if token expired or utilized
    def _isTokenActive(self, db:Dbsession, user_data:User):
        user = db.query(User).filter(
            User.id == user_data.id,
                or_(
                    User.token_expire_datetime<datetime.now(),
                    User.password_token == user_data.password_token
                ),
            ).first()
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=UserLabels.err_msg_token_expired
            )
        else:
            return True
    
    def _userExists(self, db:Dbsession, user_data:User):
        user = db.query(User).filter(
            User.id == user_data.id, 
        ).first()
        
        #if user has no result means no user exists
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=UserLabels.err_msg_record_not_found
                )
        else:
            return user
     #setting the token for password reset functionality
    def _setToken(self, user_data:User, db:Dbsession):
        now = datetime.now()
        user_data.token_expire_datetime = now + timedelta(minutes = 10)
        user_data.is_token_used = False
        db.commit()
        db.refresh(user_data)
        return user_data
    
    #SEND EMAIL TO SET PASSWORD
    def _sendPwdSetEmail(self,user_data:User):
    
        CommonFxn.sendEmail(
            {
                'from': 'abc@gmail.com',
                'to': user_data.email,
                'subject': UserLabels.pwd_set_email_subject,
                'body': UserLabels.pwd_set_email_body_template.format(password_token=user_data.password_token)
            }
        )
    