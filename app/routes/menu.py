from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemResponse


router = APIRouter()


@router.get("/", response_model=list[MenuItemResponse])
async def get_menu(
    # gives the endpoint a database session.
    db: AsyncSession = Depends(get_db),
):
# Get MenuItem records from the database
    result = await db.execute(
        select(MenuItem).where(MenuItem.is_available == True)
    )
# converts the database result into a list of MenuItem objects.
    menu_items = result.scalars().all()

# sends them back to the customer
    return menu_items