from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime, time

class CompanyBase(BaseModel):
    pass
    
#define the fields you want to use while showing response or using this class in the service
class CompanyResponse(BaseModel):
    name:str
    start_time:time
    end_time:time
    contact:Optional[str]
    email:Optional[str]
    location:Optional[str]
    model_config = ConfigDict(from_attributes =True)
    
class CompanyCreate(BaseModel):
    name:str
    start_time:time
    end_time:time
    contact:Optional[str]
    email:EmailStr
    location:Optional[str]
    description:Optional[str]
    is_active:bool
    model_config = ConfigDict(from_attributes = True)
    

class CompanyUpdate(BaseModel):
    name:Optional[str] = None
    start_time:Optional[str] = None
    end_time:Optional[str] = None
    contact:Optional[str] = None
    email:Optional[EmailStr] = None
    location:Optional[str] = None
    description:Optional[str] = None
    is_active:Optional[bool] = None
    model_config = ConfigDict(from_attributes = True)

