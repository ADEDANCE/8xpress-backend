from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

# connect OrderItem to the orders
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    # 

    menu_item_id: Mapped[int] = mapped_column(
    ForeignKey("menu_items.id")
)

    # ordered quentity
    quantity: Mapped[int]
    # price of one item
    unit_price: Mapped[float]
    # total price for that particular line item
    subtotal: Mapped[float]