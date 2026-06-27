from fastapi import APIRouter , Depends, HTTPException ,status

from schemas.company import CompanyCreate, CompanyUpdate ,CompanyResponse
from models import company,job

from sqlalchemy.orm import Session,relationship
from database import get_db, SessionLocal

router = APIRouter(prefix="/company", tags=["company"])
companies = []

@router.post("/",status_code=status.HTTP_201_CREATED,
response_model=CompanyResponse)
def create_company(company: CompanyCreate,db: Session = Depends(get_db)):
    db_company = company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/",status_code=status.HTTP_200_OK,
response_model=list[CompanyResponse])
def get_all_company(company_id: int,db: Session = Depends(get_db)):
    pass

@router.get("/{company_id}",status_code=status.HTTP_200_OK,
response_model=CompanyResponse)
def read_company(Company_id: int,db: Session = Depends(get_db)):
    pass

@router.put("/{company_id}",status_code=status.HTTP_200_OK,
response_model=CompanyResponse)
def update_company(company_id: int, company: CompanyUpdate):
    companies[company_id] = company
    return companies

@router.delete("/{company_id}",status_code=status.HTTP_200_OK)
def delete_company(company_id: int):
    companies.pop(company_id)
    return companies


