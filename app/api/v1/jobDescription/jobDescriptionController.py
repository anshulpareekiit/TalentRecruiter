from app.database.mysqlConnection import Dbsession,get_db #db mysql connection created
from . import jobDescriptionModel
from fastapi import APIRouter, status, Depends
from app.api.v1.jobDescription.jobDescriptionService import JobDescriptionService
from app.dependencies.authDependency import checkUserAuthorization
from app.entities.jobDescription import JobDescription
from sqlalchemy.orm import Session
#base route defining here so we can append other route after this
router = APIRouter(
    prefix='/v1/jobDescription', 
    tags=['JD']
)

#creating object of User Service
jobDescriptionObj = JobDescriptionService()

#####################get all users at once####################
@router.get('/',response_model=list[jobDescriptionModel.JobDescriptionResponse])
async def getAllJobDescription( db:Dbsession, 
                        skip: int = 0, 
                        limit: int = 10, 
                        auth=Depends(checkUserAuthorization)):
    return jobDescriptionObj.getJobDescription(db, skip=skip, limit=limit)

#####################create new record####################
@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def createJobDescription(jobDescription:jobDescriptionModel.JobDescriptionCreate, db:Dbsession,auth=Depends(checkUserAuthorization)):
    return jobDescriptionObj.createJobDescription(jobDescription, db)

#####################update user record####################
@router.put("/update/{jd_id}", response_model=jobDescriptionModel.JobDescriptionUpdate)
async def updateJobDescription(db:Dbsession, jd_id:int, jd_data:jobDescriptionModel.JobDescriptionUpdate, auth=Depends(checkUserAuthorization)):
    return jobDescriptionObj.updateJobDescription(db, jd_id, jd_data)

#####################get record by Id####################
@router.get("/{jd_id}}", response_model=jobDescriptionModel.JobDescriptionbyId)
async def getJobDescriptionById(db:Dbsession, jd_id:int, auth=Depends(checkUserAuthorization)):
    return jobDescriptionObj.getJobDescriptionById(db, jd_id)


@router.post('/generateJD')
async def generateJD(jd:jobDescriptionModel.JDGenerate, db:Dbsession, auth=Depends(checkUserAuthorization)):
    return await jobDescriptionObj.generateJD(jd, db)