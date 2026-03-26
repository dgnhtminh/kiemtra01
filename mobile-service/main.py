from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile Service")

@app.post("/mobiles/", response_model=schemas.MobileResponse)
def create_mobile(mobile: schemas.MobileCreate, db: Session = Depends(get_db)):
    db_mobile = models.Mobile(**mobile.dict())
    db.add(db_mobile)
    db.commit()
    db.refresh(db_mobile)
    return db_mobile

@app.get("/mobiles/", response_model=List[schemas.MobileResponse])
def read_mobiles(skip: int = 0, limit: int = 100, q: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Mobile)
    if q:
        query = query.filter(models.Mobile.brand.ilike(f"%{q}%") | models.Mobile.model.ilike(f"%{q}%"))
    return query.offset(skip).limit(limit).all()

@app.get("/mobiles/{mobile_id}", response_model=schemas.MobileResponse)
def read_mobile(mobile_id: int, db: Session = Depends(get_db)):
    mobile = db.query(models.Mobile).filter(models.Mobile.id == mobile_id).first()
    if mobile is None:
        raise HTTPException(status_code=404, detail="Mobile not found")
    return mobile
