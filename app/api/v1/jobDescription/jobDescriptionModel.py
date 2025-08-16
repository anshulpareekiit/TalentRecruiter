from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class JobDescriptionBase(BaseModel):
    pass

#define the fields you want to use while showing response or using this class in the service
class JobDescriptionResponse(BaseModel):
    company_id:int
    preferred_location:str
    primary_technology:str
    Secondary_technology:str
    years_of_experience:float
    relevant_experience:float
    notice_period:float
    job_title:str
    employment_type:str
    remote_option:bool
    generated_jd_text:str
    model_config = ConfigDict(from_attributes =True)

class JobDescriptionCreate(BaseModel):
    company_id:int
    preferred_location:str
    primary_technology:str
    Secondary_technology:str
    years_of_experience:float
    relevant_experience:float
    notice_period:float
    job_title:str
    employment_type:str
    remote_option:bool
    generated_jd_text:str

class JobDescriptionUpdate(BaseModel):
    company_id:Optional[str] = None
    preferred_location:Optional[str] = None
    primary_technology:Optional[str] = None
    Secondary_technology:Optional[str]=None
    years_of_experience:Optional[float] = None
    relevant_experience:Optional[float] = None
    notice_period:Optional[float] = None
    job_title:Optional[str] = None
    employment_type:Optional[str]=None
    remote_option:Optional[bool] = None
    generated_jd_text:Optional[str] = None

    model_config = ConfigDict(from_attributes = True)

class JobDescriptionbyId(BaseModel):
    company_id:Optional[str] = None
    preferred_location:Optional[str] = None
    primary_technology:Optional[str] = None
    Secondary_technology:Optional[str]=None
    years_of_experience:Optional[float] = None
    relevant_experience:Optional[float] = None
    notice_period:Optional[float] = None
    job_title:Optional[str] = None
    employment_type:Optional[str]=None
    remote_option:Optional[bool] = None
    generated_jd_text:Optional[str] = None
    model_config = ConfigDict(from_attributes = True)
    
class JDGenerate(BaseModel):
    preferred_location:Optional[str] = None
    primary_technology:Optional[str] = None
    Secondary_technology:Optional[str]=None
    years_of_experience:Optional[float] = None
    relevant_experience:Optional[float] = None
    notice_period:Optional[float] = None
    job_title:Optional[str] = None
    employment_type:Optional[str]=None
    remote_option:Optional[bool] = None