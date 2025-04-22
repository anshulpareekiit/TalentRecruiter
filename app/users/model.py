from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum
from typing import Optional

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
    company_id:Optional[str] = None
    password:str = Field(min_length=8, max_length=50)

class UserUpdate(BaseModel):
    email:Optional[str] = None
    mobile:Optional[str] = None
    role:Optional[UserRole] = None
    is_active:Optional[bool] = None
    company_id:Optional[str] = None
    password:Optional[str] = Field(default=None,min_length=8, max_length=50)
    model_config = ConfigDict(from_attributes = True)
    
class UserById(UserBase):
    username:Optional[str]
    f_name:Optional[str]
    l_name:Optional[str]
    model_config = ConfigDict(from_attributes =True)
