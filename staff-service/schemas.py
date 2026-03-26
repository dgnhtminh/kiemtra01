from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    serial_number: str
    status: str = "Assigned"

class ItemCreate(ItemBase):
    staff_id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    staff_id: int

    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    name: str
    department: str
    position: str

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    items: List[ItemResponse] = []

    class Config:
        orm_mode = True
