from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Staff(Base):
    __tablename__ = "staffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department = Column(String(100))
    position = Column(String(100))
    
    items = relationship("Item", back_populates="staff")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    serial_number = Column(String(100), unique=True, index=True)
    status = Column(String(50), default="Assigned") # Assigned, Returned, Maintenance
    staff_id = Column(Integer, ForeignKey("staffs.id"))
    
    staff = relationship("Staff", back_populates="items")
