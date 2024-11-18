from fastapi import FastAPI, Body, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import HTTPConnection
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn 
from typing import List, Optional 
from pydantic import Field, Base64Bytes, BaseModel
from fastapi.staticfiles import StaticFiles



app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'),name='static')



@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, host='127.0.12.1', reload=True)
