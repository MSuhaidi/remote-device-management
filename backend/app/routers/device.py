from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/devices/register", response_model=schemas.DeviceOut)
def register_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device.name)
    if db_device:
        return crud.update_device_status(db, device=db_device)
    return crud.create_device(db=db, device=device)

@router.get("/devices", response_model=List[schemas.DeviceOut])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices
