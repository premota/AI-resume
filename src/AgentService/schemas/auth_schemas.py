from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class RegisterRequest(BaseModel):
    email : EmailStr
    username : str = Field(min_length=3, max_length= 30)
    password: str = Field(min_length=8, max_length=72)

class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int 
    email : str 
    username : str 
    created_at : datetime
    