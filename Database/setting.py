from fastapi import Depends
from starlette.config import Config
from sqlmodel import SQLModel,create_engine,Field,Session
from typing import Annotated
import cloudinary # type: ignore

config = Config(".env")
db:str = config("DATABASE_URL",cast=str)

cloudinary.config(
  cloud_name = "dhsfqpxlt",
  api_key = "415496698592747",
  api_secret = "LnKk2Xwoydkchx7fjMiTfBqhhVU"
)

connection_string:str = db.replace("postgresql","postgresql+psycopg2")

engine = create_engine(connection_string,pool_pre_ping=True , echo=True, pool_recycle=300,max_overflow=0)

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION= Annotated[Session,Depends(get_session)]