from pydantic import BaseModel
from typing import Optional
class SchemaCategories(BaseModel):
    category_name:str
    category_description: Optional[str] = None