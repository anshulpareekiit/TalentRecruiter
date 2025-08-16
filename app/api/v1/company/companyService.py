from app.database.mysqlConnection import Dbsession
from . import companyModel
from fastapi import status, HTTPException
from app.entities.company import Company
from app.utils.commonFxn import CommonFxn
from app.labels.commonMsgLabels import CommonMsgLabels 
from sqlalchemy import or_, and_
from app.utils.responseHandler import success_response

###############################################################################################################################
############################CLASS CONTAINS USER RELATED FUNCTIONALITIES########################################################
##############################################################################################################################

class CompanyService:
    commonObj = CommonFxn()
    
    #######Desc: To add new company#######
    def createCompany(self,company:companyModel.CompanyCreate, db:Dbsession):
        try:
            #check for duplicate company
            self._duplicateCompany(db, company)
            #get all request data in db_user
            db_company = Company(**company.model_dump())
            db.add(db_company)
            db.commit()
            db.refresh(db_company)
            return success_response(CommonMsgLabels.msg_created_success)
        except HTTPException as e:
            db.rollback()
            # Handle the exception raised from check_duplicate_user or any inner function throwing error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.detail)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= e)
        
   
    #update company details
    def updateCompany(self, db: Dbsession, company_id: int, company_data: companyModel.CompanyUpdate):
        try:
            company_detail = db.query(Company).filter(Company.id == company_id).first()
            if company_detail is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CommonMsgLabels.err_msg_record_not_found)
            self._duplicateCompany(db,company_data,company_id=company_id)
            # Safely update only provided fields
            company_data_dict = company_data.model_dump(exclude_unset=True)
            #if field exists or not
            self._checkIfUpdateFieldExists(company_data_dict)
            for key, value in company_data_dict.items():
                #ensure if we have attr present in the model
                if hasattr(company_detail, key):
                    setattr(company_detail, key, value)
            db.commit()
            db.refresh(company_detail)
            return success_response(CommonMsgLabels.msg_update_success)

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            
    #getCompanyById()
    #db:Dbsession: db connection
    #
    # Get company details by company Id
    def getCompanyById(self,db:Dbsession,company_id:int):
        try:
            result = db.query(Company).filter(Company.id == company_id).first();
            if result != None:
                #converting response in json format
                resp = companyModel.CompanyResponse.model_validate(result).model_dump()
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=CommonMsgLabels.err_msg_record_not_found)
            return resp
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    #get companies with limit
    def getCompanies(self, db:Dbsession, skip: int = 0, limit: int = 10):
        try:
            result = db.query(Company).offset(skip).limit(limit).all();
            if result != None:
                resp = [companyModel.CompanyResponse.model_validate(res).model_dump_json() for res in result]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CommonMsgLabels.err_msg_record_not_found)
            return success_response(CommonMsgLabels.msg_record_found,resp)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=e)
        
        
        
################################################################################################################    
#############below are the private functions used for the current class ########################################
###############################################################################################################


    #return response false if duplicate not found else send json reponse for duplicate
    def _duplicateCompany(self, db:Dbsession, company:Company, company_id:int=None):
        if company_id is None:
            cond = or_(Company.email==company.email)
        else:
            cond = and_(Company.email == company.email, company_id!=Company.id)
        ##Check if duplicate records found
        if db.query(Company).filter(cond).first() != None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=CommonMsgLabels.err_msg_duplicate_rec)
            

    ###########WHEN UPDATE FIELD EXISTS#############
    def _checkIfUpdateFieldExists(self, user_data_dict:Company):
        if not user_data_dict:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=CommonMsgLabels.err_msg_field_notfound)
                
    
    