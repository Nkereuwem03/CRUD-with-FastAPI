from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import List, Union
from pydantic.types import conint

class BaseConfig(BaseModel):
    class Config:
        from_attributes = True
        
class CreateUser(BaseConfig):
    username: str
    email: EmailStr
    password: str
            
class UserPost(BaseConfig):
    id: int
    title: str
    content: str
        
class UserResponse(BaseConfig):
    id: int
    username: str
    email: EmailStr
    posts: List[UserPost] = []
        
class PostUser(BaseConfig):
    id: int
    username: str
    email: EmailStr

class UpdateUser(BaseConfig):
    email: EmailStr

class CreatePost(BaseConfig):
    title: str
    content: str

class PostResponse(BaseConfig):
    id: int
    title: str
    content: str
    date_created: datetime
    owner_id: int
    owner: Union[PostUser, None]

class PostOut(BaseConfig):
    post: PostResponse
    votes: int 

class UpdatePost(BaseConfig):
    title: str
    content: str
    
class AddVote(BaseConfig):
    blog_id: int
    dir: conint(le=1)
                  
class Token(BaseConfig):
    access_token: str
    token_type: str
    
class TokenData(BaseConfig):
    email: Union[EmailStr, None] = None