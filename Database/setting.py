from fastapi import Depends
from starlette.config import Config
from sqlmodel import SQLModel,create_engine,Field,Session
from typing import Annotated
import cloudinary # type: ignore

config = Config(".env")
db:str = config("DATABASE_URL",cast=str)
cloud_name: str = config("CLOUDINARY_CLOUD_NAME")
api_key:str= config("CLOUDINARY_API_KEY")
api_secret:str=config("CLOUDINARY_API_SECRET")
cloudinary.config(
  cloud_name = cloud_name,
  api_key = api_key,
  api_secret = api_secret
)

connection_string:str = db.replace("postgresql","postgresql+psycopg2")

engine = create_engine(connection_string,pool_pre_ping=True , echo=True, pool_recycle=300,max_overflow=0)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION= Annotated[Session,Depends(get_session)]