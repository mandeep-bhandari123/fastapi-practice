from pydantic import BaseModel,EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

class PostBase(BaseModel):
    title: str
    content: str 
    published:bool= False
    
class PostCreate(PostBase):
    pass
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode = True

class Post(BaseModel):
    owner_id:int
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner:UserOut
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes:int
    class Config:
        orm_mode = True
class UserCreate(BaseModel):

    email:EmailStr
    password:str
    
    


class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None
    


class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(ge=0,le=1)]