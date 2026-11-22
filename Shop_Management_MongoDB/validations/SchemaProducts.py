from pydantic import BaseModel, Field
from typing import Optional
import datetime

class SchemaProducts(BaseModel):
    product_name: str
    product_category: str
    product_price: float = Field(gt=0)
    product_stock: int = Field(ge=0)
    product_low_stock_limit: int = 5
    product_description: Optional[str] = None

class SchemaRestock(BaseModel):
    restock_quantity: int = Field