    
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.dependencies import get_db, get_current_user


# Create the router
router = APIRouter()


# Register endpoint
@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    # Check if the email already exists
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    # Give us the user if one exists, otherwise None
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create the new user
    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    # Add the user to the database session
    db.add(user)

    # Save the user to the database
    await db.commit()

    # Get the generated user ID
    await db.refresh(user)

    return {
        "message": "Account created successfully",
        "user_id": user.id,
    }


# Login endpoint
@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    # Find the user by email
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    # Give us the User object if one exists
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check the password
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create the login token
    access_token = create_access_token(user.id)

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "user": {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    },
}


# # Get currently logged-in user
# @router.get("/me")
# async def get_me(
#     current_user: User = Depends(get_current_user),
# ):
#     return {
#         "id": current_user.id,
#         "name": current_user.name,
#         "email": current_user.email,
#         "role": current_user.role,
#     }

