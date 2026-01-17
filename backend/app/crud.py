from sqlalchemy.orm import Session
from app import models, schemas
import datetime

def get_device_by_name(db: Session, name: str):
    return db.query(models.Device).filter(models.Device.name == name).first()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(
        name=device.name,
        last_seen=datetime.datetime.now(),
        status="online"
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device_status(db: Session, device: models.Device):
    device.last_seen = datetime.datetime.now()
    device.status = "online"
    db.commit()
    db.refresh(device)
    return device

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()
