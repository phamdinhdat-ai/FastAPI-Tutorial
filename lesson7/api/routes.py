import os
from typing import Annotated, Any 
from datetime import timedelta

from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.config import Config
from openai import OpenAI
from .crud import crud_email_log, crud_user 
from .database import get_session 
from .schemas import (EmailLogCreate, EmailLogRead, EmailRequest, EmailResponse, UserCreate, UserCreateInternal, UserRead)
from .helper import *