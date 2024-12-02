import os 
from datetime  import datetime, timedelta, timezone
from typing import Any , Annotated

import bcrypt 
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import SQLModel 
# from starlette.config import Config 
from fastapi.security import OAuth2PasswordBearer

from database import DATABASE_URL, get_session
from crud import crud_user 


# current_file_dir = os.path.dirname(os.path.realpath(__file__))
# env_path = os.path.join(current_file_dir, ".env")
# config = Config(env_path)

# # Security settings
# SECRET_KEY = config("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

UTC = timezone.utc

SECRET_KEY = "abc"
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



async def create_access_token(data:dict[str, Any], expires_delta: timedelta = None) -> str: 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else: 
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=10)
        
    to_encode.update({
        'exp':expire
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')


async def verify_token(token:str, db: AsyncSession) -> TokenData:
    try: 
        payload = jwt.decode(token=token, key= SECRET_KEY , algorithms='HS256')
        username_or_email = payload.get('sub')
        if username_or_email is None: 
            return None 
        return TokenData(username_or_email=username_or_email)
    except JWTError: 
        return None

async def authenticate_user(username_or_email: str, password: str, db: AsyncSession):
    # check email syntax 
    if '@' in username_or_email: 
        db_user: dict | None = await crud_user.get(db=db, email= username_or_email, is_deleted=False)
    else: 
        db_user: dict | None = await crud_user.get(db = db, username = username_or_email, is_deleted=False)
    
    if not db_user:
        return False
    elif not await verify_password(plain_password=password, hashed_password=db_user['hashed_password']):
        print("password is wrong")
        return False
    
    return db_user

# Dependency
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_session)]
) -> dict[str, Any] :
    """Get the current authenticated user."""
    token_data = await verify_token(token, db)
    if token_data is None:
        raise HTTPException(status_code=401, detail="User not authenticated.")

    if "@" in token_data.username_or_email:
        user = await crud_user.get(
            db=db, email=token_data.username_or_email, is_deleted=False
        )
    else:
        user = await crud_user.get(
            db=db, username=token_data.username_or_email, is_deleted=False
        )

    if user:
        return user

    raise HTTPException(status_code=401, detail="User not authenticated.")
