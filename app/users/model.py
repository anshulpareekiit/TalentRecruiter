from pydantic import BaseModel, ConfigDict
from typing import Optional
    
class UserBase(BaseModel):
    
    username:str
    f_name:str
    l_name:str
    email:str
    mobile:str
    
class UserResponse(UserBase):
    username:str
    f_name:str
    l_name:str
    email:str
    mobile:str
    model_config = ConfigDict(from_attributes =True)
    
class UserCreate(UserBase):
    username:str
    f_name:str
    l_name:str
    #email:str
    #mobile:str

class UserById(UserBase):
    username:str
    f_name:str
    l_name:str