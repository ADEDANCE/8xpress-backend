from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_admin
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemResponse


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
    current_user = Depends(require_admin),
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



@router.put("/{menu_item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    menu_item_id: int,
    data: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
    #only an admin can use this endpoint.
    current_user = Depends(require_admin),
):
    result = await db.execute(
        select(MenuItem).where(MenuItem.id == menu_item_id)
    )
# get database object.
    menu_item = result.scalar_one_or_none()
# if it doesn't exist:
    if not menu_item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )
# update the object
    menu_item.name = data.name
    menu_item.description = data.description
    menu_item.price = data.price
    menu_item.image_url = data.image_url
    menu_item.is_available = data.is_available
# saves the changes
    await db.commit()
    # gets the updated version from the database
    await db.refresh(menu_item)

    return menu_item