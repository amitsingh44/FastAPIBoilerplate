from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    id:int
    title: str
    content: str

class PostSchema(BaseModel):
    id:int
    title: str
    content: str

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title:str
    content: str

    class Congig:
        orm_mode = True