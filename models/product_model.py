from sqlmodel import SQLModel, Field, ARRAY, String
from typing import Optional
from sqlalchemy import Column


class Product(SQLModel, table=True):
    product_id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    product_description: str
    product_image: Optional[str] = None
    category_names: list[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))