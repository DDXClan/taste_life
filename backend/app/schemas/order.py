from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Dict

class OrderItem(BaseModel):
    order: Dict[int, int]

    