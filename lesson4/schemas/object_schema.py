from pydantic import BaseModel, Filed 
from typing import Dict, List, Callable, Any

class XRayRespone(BaseModel):
    probs:list = []
    best_prob:float = -1.0 
    predicted_id:int = 0 
    predicted_class:str = "" 
    predictor_name:str = "" #name of model
    
    
    
    
    
class SQLRespone(BaseModel):
    predictor_name:str = ""
    predicted_query:str = ""
    schema:Callable[..., Dict[str, Any]] = None