from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Service")

@app.post("/customers/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.get("/customers/", response_model=List[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/login", response_model=schemas.CustomerResponse)
def login(creds: schemas.CustomerLogin, db: Session = Depends(get_db)):
    db_customer = db.query(models.Customer).filter(
        models.Customer.email == creds.email, 
        models.Customer.password == creds.password
    ).first()
    if not db_customer:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_customer

@app.post("/carts/{customer_id}/items", response_model=schemas.CartItemResponse)
def add_to_cart(customer_id: int, item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.customer_id == customer_id).first()
    if not cart:
        cart = models.Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.item_id == item.item_id,
        models.CartItem.service_type == item.service_type
    ).first()
    
    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(**item.model_dump(), cart_id=cart.id)
        db.add(cart_item)
        
    db.commit()
    db.refresh(cart_item)
    return cart_item

@app.get("/carts/{customer_id}", response_model=schemas.CartResponse)
def get_cart(customer_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.customer_id == customer_id).first()
    if not cart:
        return schemas.CartResponse(id=0, customer_id=customer_id, items=[])
    return cart
