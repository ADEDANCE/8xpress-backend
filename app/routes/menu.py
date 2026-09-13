from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemResponse


router = APIRouter()


@router.get("/", response_model=list[MenuItemResponse])
async def get_menu(
    db: AsyncSession = Depends(get_db),
):
    # Get available menu items from the database
    result = await db.execute(
        select(MenuItem).where(MenuItem.is_available == True)
    )

    # Convert the database result into a list
    menu_items = result.scalars().all()

    # Send the menu items back to the customer
    return menu_items


@router.post("/")
async def create_menu_item(
    data: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
):
    # Create the database object
    menu_item = MenuItem(
        name=data.name,
        description=data.description,
        price=data.price,
        image_url=data.image_url,
    )

    # Add the item to the database session
    db.add(menu_item)

    # Save the item to PostgreSQL
    await db.commit()

    # Get the newly generated ID and other database values
    await db.refresh(menu_item)

    # Send the newly created menu item back
    return menu_item