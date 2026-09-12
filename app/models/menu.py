from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[str]
    is_available: Mapped[bool] = mapped_column(default=True)