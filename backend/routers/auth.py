from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models.users import User
from schemas.users import UserCreate, UserResponse
from schemas.token import Token
from utils.security import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# ===========================
# Register
# ===========================
@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Check if email already exists
        result = await db.execute(
            select(User).filter(User.email == user.email)
        )
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(user.password)

        # Create new user
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role
        )

        # Save user
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )


# ===========================
# Login
# ===========================
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Find user by email
        result = await db.execute(
            select(User).filter(
                User.email == form_data.username
            )
        )

        existing_user = result.scalars().first()

        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Verify password
        if not verify_password(
            form_data.password,
            existing_user.hashed_password
        ):
            raise HTTPException(
                status_code=401,
                detail="Incorrect password"
            )

        # Generate token
        access_token = create_access_token(
            data={
                "sub": str(existing_user.id),
                "role": existing_user.role
            }
        )

        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )