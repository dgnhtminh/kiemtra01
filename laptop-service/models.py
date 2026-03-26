from sqlalchemy import Column, Integer, String, Float
from database import Base

class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    specs = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
