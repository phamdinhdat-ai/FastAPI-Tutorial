import os
from typing import Annotated, Any 
from datetime import timedelta

from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.config import Config
# from openai import OpenAI
from crud import crud_email_log, crud_user 
from database import get_session 
from schemas import (EmailLogCreate, EmailLogRead, EmailRequest, EmailResponse, UserCreate, UserCreateInternal, UserRead)
from helper import create_access_token, get_current_user, get_password_hash, SECRET_KEY,get_session, Token, TokenData, authenticate_user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
#-------------path envrionment ---------------
# current_file_dir = os.path.dirname(os.path.realpath(__file__))
# env_path = os.path.join(current_file_dir, ".env")
# config = Config(env_path)

# OPENAI_API_KEY = config("OPENAI_API_KEY")

# open_ai_client = OpenAI(api_key=OPENAI_API_KEY)


# ------------- user -------------------
user_router = APIRouter()



@user_router.post("/registers/", response_model= UserRead)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    hashed_password = get_password_hash(user.password)
    user_data  = user.model_dump()
    user_data['hashed_password'] = hashed_password
    del user_data['password']
    
    # add new user 
    new_user = await crud_user.create(db=db, object= UserCreateInternal(**user_data))
    return new_user

    
@user_router.post("/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(
        username_or_email=form_data.username, 
        password=form_data.password, 
        db=db
    )
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=10)
    
    access_token = await create_access_token(
        data={"sub": user["username"]}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/", response_model=UserRead)
async def greeting():
    return {"message": "Hello World"}
