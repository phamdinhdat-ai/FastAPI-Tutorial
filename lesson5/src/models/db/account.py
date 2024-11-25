import datetime 
import sqlalchemy 
from sqlalchemy.orm import Mapper as SQLMapped
from sqlalchemy.orm import mapped_column as SQLmapped_column 

from sqlalchemy.sql import functions as sqlalchemy_functions 

from src.repository.table import Base


#create account object which store information of user
# inherite from Base table class
class Account(Base):
    __tablename__ = 'account'
    id: SQLMapped[int] = SQLmapped_column(primary_key=True, autoincrement="auto")
    username: SQLMapped[str] = SQLmapped_column(
        sqlalchemy.String(length=64), nullable=False, unique=True
    )
    email: SQLMapped[str] = SQLmapped_column(sqlalchemy.String(length=64), nullable=False, unique=True)
    _hashed_password: SQLMapped[str] = SQLmapped_column(sqlalchemy.String(length=1024), nullable=True)
    _hash_salt: SQLMapped[str] = SQLmapped_column(sqlalchemy.String(length=1024), nullable=True)
    is_verified: SQLMapped[bool] = SQLmapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    is_active: SQLMapped[bool] = SQLmapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    is_logged_in: SQLMapped[bool] = SQLmapped_column(sqlalchemy.Boolean, nullable=False, default=False)
    created_at: SQLMapped[datetime.datetime] = SQLmapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLMapped[datetime.datetime] = SQLmapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}
    
    @property 
    def hashed_password(self) -> str: 
        return self._hashed_password
    @property 
    def set_hashed_password(self, password:str) -> None:
        self._hashed_password = password
    @property 
    def hashed_salt(self) -> str: 
        return self._hash_salt
    @property
    def set_hashed_salt(self, hash_salt:str)-> None: 
        self._hash_salt = hash_salt
