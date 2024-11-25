import pydantic 
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)
# async_sessionmaker: using to manage asynchonous sesssion, helping communication between database and app easyly
#AsyncEngine: la engine khong dong bo cua SQLALchemym chiu trach nhiem giao tiep voi co so du lieu thong qua cac dirver khong dongbo 
# la thanh phan cot loi de ket noi va thuc thi cac truy van khong dong bo trong co so du lieu

from sqlalchemy.pool import Pool as SQLAlchemyPool, QueuePool as SQLAlchemyQueuePool
# Pool: la lop co ban de quan ly ket noi co so du lieu, giu cac ket noi trong mot nhom de ti su dungm giup tang hieu xuat, tranh tao ket noi moi voi moi yeu cau moi 
# QueuePool: la mot dang pool hang doi pho bien, su dung de quan ly ket noi voi co so du lieu. 
# tu dong tao casc ket noi moi khi can 
# su dung laij cac ket noi cu khi co san 
# c the giiu han so luong ket noi toi da 
#--> huu ich khi lam viec voi he thong co hieu suat cao hoac quan ly tai nguyen chat che

from src.config.manager import settings

class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = pydantic.PostgresDsn(
            url=f"{settings.DB_POSTGRES_SCHEMA}://
            {settings.DB_POSTGRES_USENRAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:
            {settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}",
            scheme=settings.DB_POSTGRES_SCHEMA,
        )
        #url:uri ket noi khong doong bo 
        #echo: nhat ky truy van 
        # pool_size: kich thuic toi da cua pool ket noi 
        # max_overflow: so luong ket noi vuot qua pool size neu can 
        # pool class: queuepool 
        
        
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=SQLAlchemyQueuePool,
        )
        self.async_session: SQLAlchemyAsyncSession = SQLAlchemyAsyncSession(bind=self.async_engine)
        self.pool: SQLAlchemyPool = self.async_engine.pool
    
    # chuyen doi uri ket noi dong bo thanh uri khong dong bo : postgresql:// ===> postgresql + asyncpg:// 
    @property
    def set_async_db_uri(self) -> str | pydantic.PostgresDsn:
        """
        Set the synchronous database driver into asynchronous version by utilizing AsyncPG:

            `postgresql://` => `postgresql+asyncpg://`
        """
        return (
            self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://")
            if self.postgres_uri
            else self.postgres_uri
        )

# doi tuong async_db: dong via tro nhu mot signleton trongh ung dung , duoc su dung toan cuc(global)
async_db: AsyncDatabase = AsyncDatabase()