from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.company import Company
from database import get_db
from utils.oauth2 import role_required, get_current_user

router = APIRouter(prefix="/job", tags=["job"])


# ---------------- CREATE JOB ---------------- #

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(role_required(["admin", "hr"]))
):
    # Verify company exists
    result = await db.execute(select(Company).where(Company.id == job.company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company not found")

    db_job = Job(**job.dict())
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job


# ---------------- GET ALL JOBS ---------------- #

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[JobResponse])
async def get_all_jobs(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


# ---------------- GET JOB BY ID ---------------- #

@router.get("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def read_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    db_job = result.scalar_one_or_none()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return db_job


# ---------------- UPDATE JOB ---------------- #

@router.put("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def update_job(
    job_id: int,
    job: JobUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(role_required(["admin", "hr"]))
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    db_job = result.scalar_one_or_none()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    update_data = job.dict(exclude_unset=True)

    if "company_id" in update_data:
        comp_result = await db.execute(select(Company).where(Company.id == update_data["company_id"]))
        if not comp_result.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company not found")

    for key, value in update_data.items():
        setattr(db_job, key, value)

    await db.commit()
    await db.refresh(db_job)
    return db_job


# ---------------- DELETE JOB ---------------- #

@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(role_required(["admin", "hr"]))
):
    result = await db.execute(select(Job).where(Job.id == job_id))
    db_job = result.scalar_one_or_none()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    await db.delete(db_job)
    await db.commit()
    return {"detail": "Job deleted successfully"}
