from sqlalchemy.orm import Session
from app import models, schemas
import datetime

def get_device_by_name(db: Session, name: str):
    return db.query(models.Device).filter(models.Device.name == name).first()

def get_device_by_id(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

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

def update_device_heartbeat(db: Session, device: models.Device):
    device.last_seen = datetime.datetime.now()
    device.status = "online"
    db.commit()
    db.refresh(device)
    return device

def update_device_status_to_offline(db: Session, device: models.Device):
    device.status = "offline"
    db.commit()
    db.refresh(device)
    return device

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()

def create_execution(db: Session, device_id: int, script_name: str) -> models.Execution:
    execution = models.Execution(
        device_id=device_id,
        script_name=script_name,
        status="pending",
        started_at=datetime.datetime.now()
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution

def get_execution(db: Session, execution_id: int):
    return db.query(models.Execution).filter(models.Execution.id == execution_id).first()

def get_executions_by_device(db: Session, device_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Execution).filter(models.Execution.device_id == device_id).offset(skip).limit(limit).all()


def get_and_start_next_pending_execution(db: Session, device_id: int):
    execution = (
        db.query(models.Execution)
        .filter(models.Execution.device_id == device_id, models.Execution.status == "pending")
        .order_by(models.Execution.started_at)
        .first()
    )
    if execution:
        execution.status = "running"
        db.commit()
        db.refresh(execution)
    return execution


def update_execution_report(db: Session, execution_id: int, report: schemas.ExecutionReport):
    execution = db.query(models.Execution).filter(models.Execution.id == execution_id).first()
    if execution:
        execution.stdout = report.stdout
        execution.stderr = report.stderr
        execution.status = report.status
        execution.finished_at = datetime.datetime.now()
        db.commit()
        db.refresh(execution)
    return execution
