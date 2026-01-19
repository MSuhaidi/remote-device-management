from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
import datetime

router = APIRouter()

@router.post("/devices/register", response_model=schemas.DeviceOut)
def register_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_name(db, name=device.name)
    if db_device:
        return crud.update_device_status(db, device=db_device)
    return crud.create_device(db=db, device=device)

@router.post("/devices/heartbeat")
def device_heartbeat(heartbeat: schemas.Heartbeat, db: Session = Depends(get_db)):
    db_device = crud.get_device_by_id(db, device_id=heartbeat.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    crud.update_device_heartbeat(db, device=db_device)
    return {"status": "ok"}

@router.get("/devices", response_model=List[schemas.DeviceOut])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    for device in devices:
        if datetime.datetime.now() - device.last_seen > datetime.timedelta(seconds=60):
            crud.update_device_status_to_offline(db, device=device)
    return devices
