from jose import jwt,JWTError
from datetime import datetime, timedelta
from schemas.token import Token
from dotenv import load_dotenv
import os
from models.users import User
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db


load_dotenv()
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        decode_token= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode_token
    except jwt.JWTError:
        return None