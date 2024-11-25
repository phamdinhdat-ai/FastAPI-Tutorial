from src.config.settings.base import BackendBaseSettings
from src.config.settings.environment import Environment

class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION:str|None = "Development Enviroment"
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    