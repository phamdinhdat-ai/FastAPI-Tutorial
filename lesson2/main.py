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
app.mount("/static", StaticFiles(directory="static"), name="static")
class Student(BaseModel):
    id: int 
    name:str = Field(None, title='name of student', max_length=20)
    subjects: List[str] = []
    
@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request, name:str):
    return templates.TemplateResponse('hello.html', {"request":request, "name":name})
    


# @app.post("/students/")
# async def student_data(st:Student):
#     return st


@app.post("/students/{college}")
async def student_data(college:str, 
                       age:int, 
                       student: Student):
    retavel = {"college": college, "age": age , **student.dict() }
    return retavel



if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, host='127.0.12.1', reload=True)
