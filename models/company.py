from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    jobs = relationship("Job", back_populates="company")