from pydantic import BaseModel
from typing import Optional

class MobileBase(BaseModel):
    brand: str
    model: str
    storage: Optional[str] = None
    color: Optional[str] = None
    price: float
    stock_quantity: int = 0

class MobileCreate(MobileBase):
    pass

class MobileResponse(MobileBase):
    id: int

    class Config:
        orm_mode = True
