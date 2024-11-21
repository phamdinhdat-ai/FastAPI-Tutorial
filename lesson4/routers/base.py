from fastapi import APIRouter
from .object_router import router as router_cls

router  = APIRouter()
router.include_router(router_cls, prefix="/Xray_prediction")
