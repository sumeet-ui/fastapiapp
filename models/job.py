from sqlalchemy import Column, Integer, String, Enum,ForeignKey
from models.company import Company
from sqlalchemy.orm import declarative_base,relationship
from database import Base , engine ,SessionLocal


Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, )
    description = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship("Company", back_populates="jobs")


