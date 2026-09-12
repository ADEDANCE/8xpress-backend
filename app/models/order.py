from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    order_type: Mapped[str] = mapped_column(String(20))

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending"
    )

    total_amount: Mapped[float]