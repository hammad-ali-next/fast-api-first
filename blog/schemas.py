# schemas.py

from datetime import datetime
from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    id: int
    title: str
    body: str
    category: str
    created_date: datetime
    image_url: str


class CreateBlog(BaseModel):
    title: str
    body: str
    category: str
    image_base64: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]


class ShowUserForBlog(BaseModel):
    name: str
    email: str


class ShowBlog(Blog):
    creator: ShowUserForBlog


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UpdateBlog(BaseModel):
    title: str
    body: str
    category: str
    image_base64: str
