from pydantic import BaseModel, Field
from typing import Optional, List

class SchemaSaleItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)

class SchemaCreateSale(BaseModel):
    customer_name: Optional[str] 
    items: List[SchemaSaleItem] = Field(min_length=1)