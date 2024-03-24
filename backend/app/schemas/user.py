from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserScheme(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None