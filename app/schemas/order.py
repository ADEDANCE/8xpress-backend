from typing import Literal

from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    order_type: Literal["pickup", "delivery"]
    phone: str
    delivery_address: str | None = None
    items: list[OrderItemCreate]





class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "confirmed",
        "preparing",
        "ready",
        "completed",
    ]