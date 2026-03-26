from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Staff Service")

@app.post("/staffs/", response_model=schemas.StaffResponse)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    db_staff = models.Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

@app.get("/staffs/{staff_id}", response_model=schemas.StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

# Nhập item
@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.id == item.staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Cập nhật item
@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
        
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
