from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.services import executor
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.post("/scripts/run", response_model=schemas.ScriptRunResponse)
def run_script_endpoint(script_run_request: schemas.ScriptRunRequest):
    try:
        execution = executor.run_script(script_name=script_run_request.script_name)
        return {"id": execution.id, "status": execution.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
