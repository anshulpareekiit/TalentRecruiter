from app.database.mysqlConnection import Dbsession
from . import usersModel
from fastapi import status, HTTPException
from app.entities.user import User
from fastapi.responses import JSONResponse
from app.utils.commonFxn import CommonFxn
import base64
from datetime import datetime, timedelta
from app.labels.userLabels import UserLabels 
from sqlalchemy import or_, and_
from app.utils.responseHandler import success_response

###############################################################################################################################
############################CLASS CONTAINS USER RELATED FUNCTIONALITIES########################################################
##############################################################################################################################

class UsersService:
    commonObj = CommonFxn()
    
    #######Desc: To add new user#######
    def createUser(self,user:usersModel.UserCreate, db:Dbsession):
        try:
            #check for duplicate user
            self._duplicateUser(db, user)
            #get all request data in db_user
            db_user = User(**user.model_dump())
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return success_response(UserLabels.msg_user_created_success)
        except HTTPException as e:
            db.rollback()
            # Handle the exception raised from check_duplicate_user or any inner function throwing error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= e)
        
    #*************send password link and set token expiry with token to be checked*****************#
    def sendPwdLink(self,db:Dbsession, user_model:usersModel.SendPwdLink):
        user_data = db.query(User).filter(User.username == user_model.username).first()
        if user_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
        try:
            user_data.password_token = base64.b64encode(user_data.email.encode('utf-8'))
            self._sendPwdSetEmail(user_data)
            self._setToken(user_data, db)
            return success_response(UserLabels.msg_email_sent_successfully)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


    ################setting up the password for user############
    def setPassword(self, db:Dbsession, user_data:usersModel.SetPassword):
        #checking if user has not used token and password token in the request matches with provided by user
        token_active = self._isTokenActive(db,user_data)
        user_exists = self._userExists(db,user_data)
        #when token is active and user found
        if token_active and user_exists is not None:
            try:
                # Safely update only provided fields
                user_data.is_token_used = True
                
                user_data.password = self.commonObj.hash_password(user_data.password)
                user_data_dict = user_data.model_dump(exclude_unset=True)
                for key, value in user_data_dict.items():
                    setattr(user_exists, key, value)
                db.commit()
                db.refresh(user_exists)
                
                return success_response(UserLabels.msg_password_set_success)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        
        
    #get all user list
    def getUsers(self, db:Dbsession, skip: int = 0, limit: int = 10):
        #check if record not found then send message
        user_cnt = db.query(User).offset(skip).limit(limit).count()
        if user_cnt <= 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
        try:
            #Fetching users
            users = db.query(User).offset(skip).limit(limit).all()
            #converting in the List
            resp = [usersModel.UserResponse.model_validate(user).model_dump() for user in users]
            #return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
            return success_response(UserLabels.msg_record_found,resp)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as exp:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exp.detail)
        


    #update user details
    def updateUser(self, db: Dbsession, user_id: int, user_data: usersModel.UserUpdate):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
            self._duplicateUser(db,user_data,user_id=user_id)
            # Safely update only provided fields
            user_data_dict = user_data.model_dump(exclude_unset=True)
            #if field exists or not
            self._checkIfUpdateFieldExists(user_data_dict)
            for key, value in user_data_dict.items():
                #ensure if we have attr present in the model
                if hasattr(user, key):
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return success_response(UserLabels.msg_update_success)

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            
    #getUserById()
    #db:Dbsession: db connection
    #
    # Get user details by user Id
    def getUserById(self,db:Dbsession, user_id:int):
        try:
            result = db.query(User).filter(User.id == user_id).first();
            if result != None:
                #converting response in json format
                resp = usersModel.UserById.model_validate(result).model_dump()
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=UserLabels.err_msg_record_not_found)
            return resp
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


################################################################################################################    
#############below are the private functions used for the current class ########################################
###############################################################################################################


    #return response false if duplicate not found else send json reponse for duplicate
    def _duplicateUser(self, db:Dbsession, user:User, user_id:int=None):
        if user_id is None:
            cond = or_(User.username==user.username, User.email == user.email)
        else:
            cond = and_(or_(User.username==user.username, User.email == user.email), user_id!=User.id)
        ##Check if duplicate records found
        if db.query(User).filter(cond).first() != None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=UserLabels.err_msg_duplicate_rec)
            

    #Check if token expired or utilized
    def _isTokenActive(self, db:Dbsession, user_data:User):
        user = db.query(User).filter(
            User.id == user_data.id,
            User.token_expire_datetime<datetime.now(),
            User.password_token == user_data.password_token
                
            ).first()
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=UserLabels.err_msg_token_expired
            )
        else:
            return True
    
    #######User exists in db ? #############
    def _userExists(self, db:Dbsession, user_data:User):
        user = db.query(User).filter(
            or_(User.id == user_data.id, User.username==user_data.username)
        ).first()
        
        #if user has no result means no user exists
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
        else:
            return user
        
    ########setting the token for password reset functionality############
    def _setToken(self, user_data:User, db:Dbsession):
        now = datetime.now()
        user_data.token_expire_datetime = now + timedelta(minutes = 10)
        user_data.is_token_used = False
        db.commit()
        db.refresh(user_data)
        return user_data
    
    ###########SEND EMAIL TO SET PASSWORD############
    def _sendPwdSetEmail(self,user_data:User):
        CommonFxn.sendEmail(
            {
                'from': 'abc@gmail.com',
                'to': user_data.email,
                'subject': UserLabels.pwd_set_email_subject,
                'body': UserLabels.pwd_set_email_body_template.format(password_token=user_data.password_token)
            }
        )
    
    ###########WHEN UPDATE FIELD EXISTS#############
    def _checkIfUpdateFieldExists(self, user_data_dict:User):
        if not user_data_dict:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=UserLabels.err_msg_field_notfound)
                
    
    