from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    
    carts = relationship("Cart", back_populates="customer")

class Cart(Base):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    
    customer = relationship("Customer", back_populates="carts")
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    item_id = Column(Integer)
    service_type = Column(String(50))
    quantity = Column(Integer, default=1)
    
    cart = relationship("Cart", back_populates="items")
