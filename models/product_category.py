from sqlmodel import SQLModel, Field
from typing import Optional


class product_categorys(SQLModel, table=True):
    category_id: Optional[int]= Field(None, primary_key=True)
    category_name: str
