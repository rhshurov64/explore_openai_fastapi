from pydantic import BaseModel
from typing import Optional


class UserCreateSchema(BaseModel):
    name: str
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    # name: Optional[str] = None
    name: str = None


class UserDetailsShowSchema(BaseModel):
    id: int
    name: str
    username: str


class CreateUserProfileSchema(BaseModel):
    user_id: int
    bio: Optional[str] = None
