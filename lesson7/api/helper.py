import os 
from datetime  import UTC, datetime, timedelta
from typing import Any , Annotated

import bcrypt 
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import SQLModel 
from starlette.config import Config 
from fastapi.security import OAuth2PasswordBearer

from .database import DATABASE_URL, get_session
from .crud import crud_user 


# current_file_dir = os.path.dirname(os.path.realpath(__file__))
# env_path = os.path.join(current_file_dir, ".env")
# config = Config(env_path)

# # Security settings
# SECRET_KEY = config("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



SECRET_KEY = ""
class Token(SQLModel):
    access_token: str 
    token_type: str 

class TokenData(SQLModel):
    username_or_email:str 

#verify plain password against a hashed password
async def verify_password(plain_password:str, hashed_password:str):
    
    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()



async def create_asscess_token(data:dict[str, Any], expires_delta: timedelta|None = None) -> str: 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else: 
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=10)
        
    to_encode.update({
        'exp':expire
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')


async def verify_token(token:str, db: AsyncSession):
    pass 