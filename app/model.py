from datetime import datetime

from pydantic import BaseModel
from typing import List, Union, Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool = False

class UserInDB(User):
    hashed_password: str

class SaladOderForm(BaseModel):
    title: str
    content: str
    menu1: str
    menu2: str
    days: List[int]

class SaladOrder(BaseModel):
    orderer: str
    email: str
    order = List[Union[str,int]]
    is_paid: bool

    class Config:
        arbitrary_types_allowed = True

class Post(BaseModel):
    writer: str
    title: str
    content: str
    created_at: Optional[str] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_at: Optional[str] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


fake_users_db = {
    # password = 1234
    "42maru": {
        "username": "42maru",
        "email": "42maru@42maru.com",
        "password":"42maru",
        "hashed_password": "$2b$12$u.o7bC5LyoYCp6vOXa6UCOEdhSmysa.mFwHDH26X0SZiDGuUd.PCu",
        "disabled": False,
    }
}