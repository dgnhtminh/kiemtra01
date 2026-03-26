from sqlalchemy import Column, Integer, String, Float
from database import Base

class Mobile(Base):
    __tablename__ = "mobiles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    storage = Column(String)
    color = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
