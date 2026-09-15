from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import verify_token
from app.database.database import AsyncSessionLocal
from app.models.user import User

# "For endpoints that use this dependency, expect a Bearer token
security = HTTPBearer()

# creates a database session for the request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:

    user_id = verify_token(credentials)

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:

     if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

        return current_user




async def require_customer(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role != "customer":
        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )

    return current_user