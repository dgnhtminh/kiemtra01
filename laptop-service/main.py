from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Laptop Service")

@app.post("/laptops/", response_model=schemas.LaptopResponse)
def create_laptop(laptop: schemas.LaptopCreate, db: Session = Depends(get_db)):
    db_laptop = models.Laptop(**laptop.dict())
    db.add(db_laptop)
    db.commit()
    db.refresh(db_laptop)
    return db_laptop

@app.get("/laptops/", response_model=List[schemas.LaptopResponse])
def read_laptops(skip: int = 0, limit: int = 100, q: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Laptop)
    if q:
        query = query.filter(models.Laptop.brand.ilike(f"%{q}%") | models.Laptop.model.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()

@app.get("/laptops/{laptop_id}", response_model=schemas.LaptopResponse)
def read_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = db.query(models.Laptop).filter(models.Laptop.id == laptop_id).first()
    if laptop is None:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop
