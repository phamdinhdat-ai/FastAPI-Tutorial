import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent)) # get parent path

from fastapi import File, UploadFile #  upload and store file
from fastapi import APIRouter
from schemas.object_schema import XRayRespone # get format response
from configs.base_cfg import XrayDataConfig, XrayModelConfig
from  schemas.object_schema import XRayRespone
from models.predictors import Predictor

router = APIRouter()
predictor = Predictor(
    model_name=XrayModelConfig.MODEL_NAME,
    model_weight=XrayModelConfig.MODEL_WEIGHT,
    device = XrayModelConfig.DEVICE
)

@router.post("/predict")
async def predict(file_upload: UploadFile = File(...)):
    response = await predictor.predict(file_upload.file)
    
    return XRayRespone(**response)