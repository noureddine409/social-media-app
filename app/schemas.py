
from datetime import datetime
from time import timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class Token_data(BaseModel):
    id: Optional[str] = None


class vote(BaseModel):
    post_id: int
    dir: conint(le=1)
