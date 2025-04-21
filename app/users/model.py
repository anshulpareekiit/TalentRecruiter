from pydantic import BaseModel, ConfigDict, EmailStr, constr
from typing import Optional
    
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
    password:str

class UserUpdate(UserBase):
    username:str
    f_name:str
    l_name:str
    email:str
    mobile:str

class UserById(UserBase):
    username:Optional[str]
    f_name:Optional[str]
    l_name:Optional[str]
    model_config = ConfigDict(from_attributes =True)
