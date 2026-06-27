from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from models.company import Company
from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    title:str
    salary:int
    description:Optional[str]=None
    company_id:int

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    title:Optional[str]=None
    salary:Optional[int]=None
    description:Optional[str]=None
    company_id:Optional[int]=None
  
class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True

