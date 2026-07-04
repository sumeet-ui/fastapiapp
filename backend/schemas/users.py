from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    class Config:
        from_attributes = True

class Login_User(BaseModel):
    email: str
    password: str