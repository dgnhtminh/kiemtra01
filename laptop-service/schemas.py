from pydantic import BaseModel
from typing import Optional

class LaptopBase(BaseModel):
    brand: str
    model: str
    specs: Optional[str] = None
    price: float
    stock_quantity: int = 0

class LaptopCreate(LaptopBase):
    pass

class LaptopResponse(LaptopBase):
    id: int

    class Config:
        orm_mode = True
