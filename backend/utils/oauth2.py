from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.token import verify_access_token
from fastapi import HTTPException
from database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str=Depends(oauth2_scheme),db:Session =Depends(get_db)):
    user_info = verify_access_token(token)
    current_user = verify_access_token(token)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    return current_user


def role_required(roles:list):
    def role_decorator(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Access Denied")
        return current_user

    return role_decorator



    