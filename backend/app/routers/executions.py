from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/executions/{execution_id}", response_model=schemas.ExecutionOut)
def read_execution(execution_id: int, db: Session = Depends(get_db)):
    db_execution = crud.get_execution(db, execution_id=execution_id)
    if db_execution is None:
        raise HTTPException(status_code=404, detail="Execution not found")
    return db_execution
