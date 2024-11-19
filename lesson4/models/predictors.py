import sys
import torch 
import torch.nn as nn 
import torchvision
from torchvision.transforms import transforms
from models.basemodels import XrayModel
from configs.base_cfg import XrayDataConfig, XrayModelConfig
class XrayPredictor:
    def __init__(self, model_name:str, 
                    model_weights:str, 
                    device:str='cpu'):
        self.model_name = model_name 
        self.model_weights = model_weights
        self.device = device
        self.model = self.load_model()
    
    
        #load model
        #create preprocesiing
    def load_model(self):
        model = XrayModel(n_classes=XrayDataConfig.N_CLASSES)
        model.load_state_dict(torch.load(self.model_weights, map_location=self.device))