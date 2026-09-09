from sqlalchemy import String,Integer,Boolean,Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    pass

class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[str]
    is_available: Mapped[bool] = mapped_column(default=True)