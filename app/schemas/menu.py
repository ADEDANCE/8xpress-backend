from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str


class MenuItemUpdate(BaseModel):
    name: str
    description: str
    price: float
    image_url: str
    is_available: bool



class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str
    is_available: bool