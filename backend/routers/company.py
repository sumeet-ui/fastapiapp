from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.company import Company
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from utils.oauth2 import get_current_user, role_required

router = APIRouter(
    prefix="/company",
    tags=["company"]
)


# ---------------- CREATE COMPANY ---------------- #

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CompanyResponse
)
async def create_company(
    company: CompanyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):
    try:
        db_company = Company(**company.dict())

        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)

        return db_company

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating company: {str(e)}"
        )


# ---------------- GET ALL COMPANIES ---------------- #

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[CompanyResponse]
)
async def get_all_company(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        result = await db.execute(select(Company))
        companies = result.scalars().all()

        return companies

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error retrieving companies: {str(e)}"
        )


# ---------------- GET COMPANY BY ID ---------------- #

@router.get(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyResponse
)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )

    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return company


# ---------------- UPDATE COMPANY ---------------- #

@router.put(
    "/{company_id}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyResponse
)
async def update_company(
    company_id: int,
    company: CompanyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )

    db_company = result.scalar_one_or_none()

    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    for key, value in company.dict(exclude_unset=True).items():
        setattr(db_company, key, value)

    await db.commit()
    await db.refresh(db_company)

    return db_company


# ---------------- DELETE COMPANY ---------------- #

@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_company(
    company_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(
        select(Company).where(Company.id == company_id)
    )

    db_company = result.scalar_one_or_none()

    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    await db.delete(db_company)
    await db.commit()

    return None