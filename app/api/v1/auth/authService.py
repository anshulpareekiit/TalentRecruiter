from app.database.mysqlConnection import Dbsession
from app.entities.userSessionToken import UserSessionToken
from app.utils.commonFxn import CommonFxn
from app.api.v1.users.usersService import UsersService
import base64
from app.entities.user import User
from sqlalchemy import or_, and_
from app.labels.authLabels import AuthLabels
from app.utils.responseHandler import success_response
from fastapi import status, HTTPException, Depends, Header
from . import authModel
from datetime import timedelta, datetime
import random
from typing import Optional
from sqlalchemy.orm import Session

###############################################################################################################################
############################CLASS CONTAINS USER RELATED FUNCTIONALITIES########################################################
##############################################################################################################################

class AuthService:
    commonObj = CommonFxn()
    userObj = UsersService()
    
    #validate user
    def validateUser(self, db, credentials:authModel.AuthicateUser):
        try:
            #match credentials email and password
            userDetails = db.query(User).filter(User.email==credentials.email, User.is_active == True).first()
            if userDetails is None:
                #raise exception if invalid user pass found
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=AuthLabels.err_msg_user_not_found)
            else:
                chk_pwd = self.commonObj.check_password(userDetails.password, credentials.password)
                if chk_pwd:
                    
                    token_detail = self._createRetSessionToken(userDetails,db)
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthLabels.err_msg_invalid_credential)
            return success_response(AuthLabels.msg_successfully_login, data={"token":token_detail})
            #user = db.query(User).filter(User.email==credentials.email).count()
        except HTTPException as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= e)
        
    #creating if needed otherwise returning the current token if exists
    def _createRetSessionToken(self, userDetails, db):
        try:
            token_detail = db.query(UserSessionToken).filter(UserSessionToken.user_id==userDetails.id, UserSessionToken.token_expiry>=datetime.now()).first()
            if token_detail is not None:
                token = token_detail.token
            else:
                #getting details from user table
                # Encode email to base64 token
                token_dem = userDetails.email+""+ str(random.randrange(101,999,1))
                token = base64.b64encode(token_dem.encode()).decode()
                #setting details to the Auth Save Token obj            
                session_data = authModel.AuthSaveToken(
                    token= token,
                    token_expiry= datetime.now() + timedelta(minutes=10),
                    user_id=userDetails.id
                )
                db_user = UserSessionToken(**session_data.model_dump())
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                token = db_user.token
            return token

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
