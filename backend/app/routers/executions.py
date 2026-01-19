from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/devices/{device_id}/executions", response_model=list[schemas.ExecutionOut])
def read_executions_by_device(device_id: int, db: Session = Depends(get_db)):
    executions = crud.get_executions_by_device(db, device_id=device_id)
    return executions

@router.get("/executions/{execution_id}", response_model=schemas.ExecutionOut)
def read_execution(execution_id: int, db: Session = Depends(get_db)):
    db_execution = crud.get_execution(db, execution_id=execution_id)
    if db_execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    return db_execution


@router.post("/devices/{device_id}/jobs/next", response_model=schemas.JobResponse, status_code=200)
def get_next_job_for_device(device_id: int, db: Session = Depends(get_db)):
    job = crud.get_and_start_next_pending_execution(db, device_id=device_id)
    if not job:
        raise HTTPException(status_code=204, detail="No pending jobs")
    return job


@router.post("/executions/{execution_id}/report", status_code=200)
def submit_execution_report(
    execution_id: int, report: schemas.ExecutionReport, db: Session = Depends(get_db)
):
    updated_execution = crud.update_execution_report(
        db, execution_id=execution_id, report=report
    )
    if not updated_execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {"status": "ok"}
