from app.database.mysqlConnection import Dbsession,get_db #db mysql connection created
from . import companyModel
from fastapi import APIRouter, status, Depends
from app.api.v1.company.companyService import CompanyService
from app.utils.authDependency import checkUserAuthorization
from app.entities.company import Company
from sqlalchemy.orm import Session
#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/v1/company', 
    tags=['companies']
)

#creating object of User Service
companyServiceObj = CompanyService()

#####################get all users at once####################
@router.get('/',response_model=list[companyModel.CompanyResponse])
async def getAllCompanies( db:Dbsession, 
                        skip: int = 0, 
                        limit: int = 10, 
                        auth=Depends(checkUserAuthorization)):
    return companyServiceObj.getCompanyById(db, skip=skip, limit=limit)

#####################create new record####################
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createCompany(company:companyModel.CompanyCreate, db:Dbsession,auth=Depends(checkUserAuthorization)):
    return companyServiceObj.createCompany(company,db)

#####################update company record####################
@router.put("/update/{company_id}", response_model=companyModel.CompanyBase)
async def updateCompany(db:Dbsession, company_id:int, company_update:companyModel.CompanyUpdate,auth=Depends(checkUserAuthorization)):
    return companyServiceObj.updateCompany(db,company_id, company_update)
    
#####################get record by Id####################
@router.get("/{company_id}", response_model=companyModel.CompanyResponse)
async def getCompanyById(db:Dbsession, company_id:int,auth=Depends(checkUserAuthorization)):
    return companyServiceObj.getCompanyById(db,company_id)
