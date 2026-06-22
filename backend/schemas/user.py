from pydantic import EmailStr
from backend.schemas.base import BaseSchema, BaseModel

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(BaseSchema, UserBase):
    pass
