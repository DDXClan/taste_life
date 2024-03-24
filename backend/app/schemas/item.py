from pydantic import BaseModel, validator
from typing import Optional

class CategoryScheme(BaseModel):
    category_name: str

class ItemScheme(BaseModel):
    item_name: Optional[str] = None
    wt: Optional[int] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category_id: Optional[int] = None

    @validator('wt')
    def check_wt(cls, wt):
        if wt < 0:
            raise ValueError('wt cannot be negative')
        return wt
    
    @validator('price')
    def check_price(cls, price):
        if price < 0:
            raise ValueError('price cannot be negative')
        return price