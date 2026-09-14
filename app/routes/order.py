from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_customer
from app.models.menu import MenuItem
from app.models.order import Order
from app.models.OrderItem import OrderItem
from app.schemas.order import OrderCreate

# create router 
router = APIRouter()


@router.post("/")
async def create_order(
    # get order
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    # get authorize user
    current_user = Depends(require_customer),
):
    total_amount = 0
    order_items = []

    for item in data.items:

        result = await db.execute(
            select(MenuItem).where(
                MenuItem.id == item.menu_item_id
            )
        )

# get menu item
        menu_item = result.scalar_one_or_none()

# Check if it exists
        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item.menu_item_id} not found"
            )

# check if item is available
        if not menu_item.is_available:
            raise HTTPException(
                status_code=400,
                detail=f"{menu_item.name} is currently unavailable"
            )
# Calculate subtotal
        subtotal = menu_item.price * item.quantity
# Add to total
        total_amount += subtotal

        order_item = OrderItem(
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            unit_price=menu_item.price,
            subtotal=subtotal,
        )

        order_items.append(order_item)

# Create the main Order
    order = Order(
        user_id=current_user.id,
        order_type=data.order_type,
        total_amount=total_amount,
    )

    db.add(order)
# Get database-generated values
    await db.flush()

# Loop through the order items
    for order_item in order_items:
        order_item.order_id = order.id
        db.add(order_item)
# save 
    await db.commit()

    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
    }