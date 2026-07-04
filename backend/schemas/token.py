from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "your_secret_key", algorithm="HS256")
    return encoded_jwt