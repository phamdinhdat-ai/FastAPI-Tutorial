# import fastapi 
from fastapi import FastAPI, Path, Query
import uvicorn
from typing import List
from pydantic import BaseModel, Field



app = FastAPI()

@app.get("/")
async def root():
    return {'message': "Helllo World"}

# @app.get('/{name}/{age}')
# async def hello(name, age:int):
    
#     return {'name': name, 'age':age}

class Student(BaseModel):
    id: int 
    name:str = Field(None, title='name of student', max_length=20)
    subjects: List[str] = []
    
    
    


# from fastapi import FastAPI, Path, Query
@app.get("/hello/{name}/{age}")
async def hello(*, name: str=Path(...,min_length=3 ,
    max_length=10), \
    age: int = Path(..., ge=1, le=100), \
    percent:float=Query(..., ge=0, le=100)):
    return {"name": name, "age":age}



@app.post("/students/{college}")
async def student_data(college:str, 
                       age:int, 
                       student: Student):
    retavel = {"college": college, "age": age , **student.dict() }
    return retavel


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
    
    