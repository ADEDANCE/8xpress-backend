from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import (
    get_db,
    require_customer,
    require_admin,
)
from app.models.menu import MenuItem
from app.models.order import Order
from app.models.OrderItem import OrderItem
from app.models.user import User
from app.schemas.order import OrderCreate, OrderStatusUpdate



# create router 
router = APIRouter()


@router.post("/")
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_customer),
):

    # Validate delivery address
    if data.order_type == "delivery" and not data.delivery_address:
        raise HTTPException(
            status_code=400,
            detail="Delivery address is required for delivery orders"
        )

    total_amount = 0
    order_items = []

    for item in data.items:

        result = await db.execute(
            select(MenuItem).where(
                MenuItem.id == item.menu_item_id
            )
        )

        menu_item = result.scalar_one_or_none()

        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {item.menu_item_id} not found"
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=400,
                detail=f"{menu_item.name} is currently unavailable"
            )

        # Calculate subtotal
        subtotal = menu_item.price * item.quantity

        # Add subtotal to order total
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
        phone=data.phone,
        delivery_address=data.delivery_address,
        total_amount=total_amount,
    )

    db.add(order)

    # Get database-generated order ID
    await db.flush()

    # Add each order item
    for order_item in order_items:
        order_item.order_id = order.id
        db.add(order_item)

    # Save everything
    await db.commit()

    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
    }



@router.get("/")
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin),
):
    result = await db.execute(select(Order))
    orders = result.scalars().all()

    response = []

    for order in orders:

        # Get customer
        result = await db.execute(
            select(User).where(User.id == order.user_id)
        )
        customer = result.scalar_one_or_none()

        # Get items belonging to this order
        result = await db.execute(
            select(OrderItem).where(
                OrderItem.order_id == order.id
            )
        )
        order_items = result.scalars().all()

        items_response = []

        for item in order_items:

            # Get menu item details
            result = await db.execute(
                select(MenuItem).where(
                    MenuItem.id == item.menu_item_id
                )
            )
            menu_item = result.scalar_one_or_none()

            items_response.append({
                "menu_item_id": item.menu_item_id,
                "name": menu_item.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
            })

        response.append({
            "order_id": order.id,

            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
            },

            "phone": order.phone,
            "order_type": order.order_type,
            "delivery_address": order.delivery_address,
            "status": order.status,
            "total_amount": order.total_amount,
            "items": items_response,
        })

    return response


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    # only an admin can change an order's status
    current_user = Depends(require_admin),
):
# Find the order
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
# Change the status
    order.status = data.status
# Save it
    await db.commit()
    await db.refresh(order)

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "status": order.status,
    }



@router.get("/my-orders")
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    # Allow Only authenticated customers
    current_user = Depends(require_customer),
):
    result = await db.execute(
        select(Order).where(
            Order.user_id == current_user.id
        )
    )

    orders = result.scalars().all()

    response = []

    for order in orders:

        result = await db.execute(
            # find the individual foods belonging to the order
            select(OrderItem).where(
                OrderItem.order_id == order.id
            )
        )

        order_items = result.scalars().all()

        items_response = []

        for item in order_items:

            result = await db.execute(
                select(MenuItem).where(
                    MenuItem.id == item.menu_item_id
                )
            )

            menu_item = result.scalar_one_or_none()

            items_response.append({
                "menu_item_id": item.menu_item_id,
                "name": menu_item.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
            })

        response.append({
    "order_id": order.id,
    "order_type": order.order_type,
    "phone": order.phone,
    "delivery_address": order.delivery_address,
    "status": order.status,
    "total_amount": order.total_amount,
    "items": items_response
})

    return response
