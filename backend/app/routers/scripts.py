from fastapi import APIRouter, Depends, HTTPException
from app import schemas, crud
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/scripts/run", response_model=schemas.ExecutionOut)
def run_script_endpoint(script_create_request: schemas.ExecutionCreate, db: Session = Depends(get_db)):
    device = crud.get_device_by_id(db, device_id=script_create_request.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    execution = crud.create_execution(
        db,
        device_id=script_create_request.device_id,
        script_name=script_create_request.script_name,
    )
    return execution
