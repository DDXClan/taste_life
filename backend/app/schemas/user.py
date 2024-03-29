from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserScheme(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @validator('password')
    def check_pass(cls, password):
        if len(password) <= 6:
                raise ValueError('Must contain more than 6 characters')
        return password

