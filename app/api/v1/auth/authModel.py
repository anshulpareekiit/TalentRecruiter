from pydantic import BaseModel, ConfigDict, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class AuthBase(BaseModel):
    pass
    
#define the fields you want to use while showing response or using this class in the service
class AuthicateUser(BaseModel):
    username:Optional[str]=None
    email:EmailStr
    password:str
    model_config = ConfigDict(from_attributes =True)
    
class AuthResponse(BaseModel):
    token:str
    model_config = ConfigDict(from_attributes=True)
    
class AuthSaveToken(BaseModel):
    token:str
    user_id:int
    token_expiry:datetime
    

