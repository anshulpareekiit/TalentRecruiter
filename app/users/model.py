from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    super_admin = 'super_admin'
    company_user = 'company_user'

class UserBase(BaseModel):
    pass
    
#define the fields you want to use while showing response or using this class in the service
class UserResponse(BaseModel):
    username:str
    f_name:str
    l_name:str
    mobile:Optional[str]
    email:Optional[str]
    model_config = ConfigDict(from_attributes =True)
    
class UserCreate(BaseModel):
    username:str
    f_name:str
    l_name:str
    email:EmailStr
    mobile:str
    role:UserRole
    is_active:bool = True
    
#req Input for send password link
class SendPwdLink(BaseModel):
    username:str    
    
class SetPassword(BaseModel):
    id:int
    password:str
    password_token:str
    is_token_used:bool=None
                       
class UserUpdate(BaseModel):
    username:Optional[str]
    email:Optional[str] = None
    mobile:Optional[str] = None
    role:Optional[UserRole] = None
    is_active:Optional[bool] = None
    company_id:Optional[str] = None
    model_config = ConfigDict(from_attributes = True)
    
class UserById(UserBase):
    username:Optional[str]
    f_name:Optional[str]
    l_name:Optional[str]
    model_config = ConfigDict(from_attributes =True)
