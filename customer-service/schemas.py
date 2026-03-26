from pydantic import BaseModel
from typing import Optional, List

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    password: str

class CustomerLogin(BaseModel):
    email: str
    password: str

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    item_id: int
    service_type: str
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    customer_id: int
    items: List[CartItemResponse] = []
    class Config:
        from_attributes = True
