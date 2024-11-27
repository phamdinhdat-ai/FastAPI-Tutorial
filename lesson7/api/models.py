from sqlmodel import SQLModel,Field
from pydantic import EmailStr
from typing import Optional 

# define abstraction for our database
class User(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True )
    username: Optional[str] = Field(..., min_length=2 , max_length=40)
    name: str = Field(..., min_length=2, max_length=20)
    email: str # EmailStr
    hashed_password:str 
    
class EmailLog(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key=True)
    user_input: str 
    reply_to: Optional[str]  = Field(default=None)
    context: Optional[str] = Field(default=None)
    length: Optional[str] = Field(default=None)
    tone: str 
    generated_email:str 
    timestamp: str 
