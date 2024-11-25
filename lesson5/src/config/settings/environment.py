import enum 

class Environment(str, enum.Enum):
    PRODUCTION:str = 'PRO'
    DEVELOPMENT: str = "DEV"
    STATGING: str = "STAGE"
