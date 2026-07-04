from fastapi import APIRouter, Depends, HTTPException, status

from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.company import Company
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import role_required,get_current_user

router = APIRouter(prefix="/job", tags=["job"])

@router.post("/", status_code=status.HTTP_201_CREATED,
response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db),current_user = Depends(role_required(["admin","hr"]))):
    company = db.query(Company).filter(Company.id == job.company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company not found")
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", status_code=status.HTTP_200_OK,
response_model=list[JobResponse])
def get_all_jobs(
    skip: int = 0,
    limit: int = 10,
    search: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(Job)
    
    # Search filter
    if search:
        query = query.filter(Job.title.ilike(f"%{search}%"))
    
    # Pagination
    jobs = query.offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", status_code=status.HTTP_200_OK,
response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job

@router.put("/{job_id}", status_code=status.HTTP_200_OK,
response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db),current_user = Depends(role_required(["admin","hr"]))):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    # pyrefly: ignore [deprecated]
    update_data = job.dict(exclude_unset=True)
    if "company_id" in update_data:
        company = db.query(Company).filter(Company.id == update_data["company_id"]).first()
        if not company:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company not found")
    for key, value in update_data.items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
def delete_job(job_id: int, db: Session = Depends(get_db),current_user = Depends(role_required(["admin","hr"]))):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"detail": "Job deleted successfully"}

