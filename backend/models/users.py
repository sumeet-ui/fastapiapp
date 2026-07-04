from database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(225), nullable=False)
    email = Column(String(225), unique=True, nullable=False)
    hashed_password = Column(String(225), nullable=False)
    role = Column(String(225), nullable=False,default="Candidate")