from app.database.mysqlConnection import Dbsession
from . import jobDescriptionModel
from fastapi import status, HTTPException
from app.entities.jobDescription import JobDescription
from fastapi.responses import JSONResponse
from app.utils.commonFxn import CommonFxn
import base64
from datetime import datetime, timedelta
from app.labels.userLabels import UserLabels 
from sqlalchemy import or_, and_
from app.utils.responseHandler import success_response
from app.api.v1.llmCall.llmCallController import chat
from app.aiModels.groqReqRes import GroqLLM
###############################################################################################################################
############################CLASS CONTAINS USER RELATED FUNCTIONALITIES########################################################
##############################################################################################################################

class JobDescriptionService:
    commonObj = CommonFxn()
    
    #######Desc: To add new user#######
    def createJobDescription(self,jd:jobDescriptionModel.JobDescriptionCreate, db:Dbsession):
        try:
            #get all request data in db_jd
            db_jd = JobDescription(**jd.model_dump())
            db.add(db_jd)
            db.commit()
            db.refresh(db_jd)
            return success_response(UserLabels.msg_user_created_success)
        except HTTPException as e:
            db.rollback()
            # Handle the exception raised from check_duplicate_user or any inner function throwing error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= e)
    
        
    #get list
    def getJobDescription(self, db:Dbsession, skip: int = 0, limit: int = 10):
        #check if record not found then send message
        user_cnt = db.query(JobDescription).offset(skip).limit(limit).count()
        if user_cnt <= 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
        try:
            #Fetching users
            users = db.query(JobDescription).offset(skip).limit(limit).all()
            #converting in the List
            resp = [jobDescriptionModel.UserResponse.model_validate(user).model_dump() for user in users]
            #return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
            return success_response(UserLabels.msg_record_found,resp)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as exp:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exp.detail)
        


    #update JobDescription Details
    def updateJobDescription(self, db: Dbsession, jd_id: int, data: jobDescriptionModel.JobDescriptionUpdate):
        try:
            jd = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
            if jd is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserLabels.err_msg_record_not_found)
            self._duplicateUser(db,data,jd_id=jd_id)
            # Safely update only provided fields
            jd_data_dict = data.model_dump(exclude_unset=True)
            #if field exists or not
            self._checkIfUpdateFieldExists(jd_data_dict)
            for key, value in jd_data_dict.items():
                #ensure if we have attr present in the model
                if hasattr(jd, key):
                    setattr(jd, key, value)
            db.commit()
            db.refresh(jd)
            return success_response(UserLabels.msg_update_success)

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            
    #getUserById()
    #db:Dbsession: db connection
    #
    # Get user details by user Id
    def getJobDescriptionById(self,db:Dbsession, jd_id:int):
        try:
            result = db.query(JobDescription).filter(JobDescription.id == jd_id).first();
            if result != None:
                #converting response in json format
                resp = jobDescriptionModel.JobDescriptionbyId.model_validate(result).model_dump()
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=UserLabels.err_msg_record_not_found)
            return resp
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


################################################################################################################    
#############      Below are the private functions to call LLM class    ########################################
################################################################################################################
    async def generateJD(self, jd, db:Dbsession):
        try:
            
            fields=jd.model_dump(exclude_unset=True)
            field_text = "\n".join(f"{key}: {value}" for key, value in fields.items())
            prompt = (
                "You are the HR of my company. Prepare a job description (JD) using the provided fields to hire a candidate."
                f"{field_text}\n"
                "Respond only with the JD text not anything else in . Do not include any extra commentary or entertain other requests.**JSON format**"
            )
            print(prompt);
            message = [
                {
                    "role": "user", 
                    "content": prompt
                }
            ];
            groqLLMObj = GroqLLM()
            resp = await groqLLMObj.chat(message)
            return resp
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)