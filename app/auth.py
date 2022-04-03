from datetime import datetime, timedelta

from fastapi import status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

from model import fake_users_db, UserInDB
from config import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_user(req:Request):
    token = None
    authorization = req.headers.get('authorization')
    if authorization:
        token_type, token = authorization.split(" ")
        if token_type=="Bearer":
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            try:
                payload = jwt.decode(token, config.secret_key, algorithms=[config.sign_algorithm])
                username: str = payload.get("sub")
                if username is None:
                    raise credentials_exception
            except JWTError:
                raise credentials_exception
            user = get_user(fake_users_db, username=username)
            if user is None:
                raise credentials_exception
            return user
        else:
            raise credentials_exception
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.sign_algorithm)
    return encoded_jwt