# app/db.py

from pydantic import BaseModel
import datetime
from typing import Optional
# from datetime import datetime

from .config import settings

class Text_Input(BaseModel):
    text: str
    
class UserBase(BaseModel):
    name: Optional[str]
    email: Optional[str]
    major: Optional[str]
    personal_statement: Optional[str]
    active: Optional[bool]


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    id: int


class UserResponse(BaseModel):
    user_id: int
    spreaker: str ='user'
    session: int
    turn: int
    transcript:str

class SystemResponse(BaseModel):
    user_id: int
    speaker: str = 'system'
    session: int
    turn: int
    transcript:str
 
