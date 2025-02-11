from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TaskResult(BaseModel):
    id: int
    url: str
    title: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: int
    status: str
    result: List[TaskResult] = []

    class Config:
        orm_mode = True