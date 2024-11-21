import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from fastapi import FastAPI
from middleware.http   import LogMiddleware
from middleware.cors import setup_cors
from routers.base import router

app = FastAPI()
setup_cors(app)
app.include_router(router)