from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict

class OrderItem(BaseModel):
    order: Dict[int, int]


class OrderUpdateStatus(BaseModel):
    unique_key: str
    order_status: int

class BasketItem(BaseModel):
    item_id: int
    quantity: int = 1