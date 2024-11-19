import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent)) # get parent path

from fastapi import File, UploadFile #  upload and store file
from fastapi import APIRouter
from schemas.object_schema import XRayRespone # get format response
from configs.base_cfg import XrayDataConfig, XrayModelConfig

