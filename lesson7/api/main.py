from fastapi import FastAPI
from database import create_async_engine, create_db_and_tables
import uvicorn
from routes import user_router
async def lifespan(app):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(user_router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)