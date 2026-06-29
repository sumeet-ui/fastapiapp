from os import name

from fastapi import APIRouter, HTTPException, Depends, status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from sqlalchemy.orm import Session
from database import get_db,SessionLocal

router = APIRouter(prefix="/company", tags=["company"])
companies = []

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/",status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
def get_all_company(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company-id()).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Company not found")
    return company
 
@router.put("/{company_id}", status_code=status.HTTP_201_CREATED)
def update_company(company_id: int, company: CompanyUpdate):
    companies[company_id] = company
    return companies

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int):
    companies.pop(company_id)
    return companies

# @router.get("/")
# def read_company():
#     return {"company": "Company root"}

# @router.get("/{company_id}")
# def read_company_by_id(company_id: int):
#     return {"company_id": company_id}