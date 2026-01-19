import subprocess
import datetime
from sqlalchemy.orm import Session
from app import crud
from app.database import SessionLocal
from app.models import Execution

ALLOWED_SCRIPTS = {
    "health_check": ["echo", "OK"],
    "echo_test": ["echo", "hello world"],
    "fail_test": ["bash", "-c", "exit 1"]
}

def run_script(script_name: str) -> Execution:
    if script_name not in ALLOWED_SCRIPTS:
        raise ValueError("Script not allowed")

    db: Session = SessionLocal()
    execution = crud.create_execution(db, script_name=script_name)
    execution.status = "running"
    db.commit()

    try:
        command = ALLOWED_SCRIPTS[script_name]
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        execution.stdout = process.stdout
        execution.stderr = process.stderr
        execution.status = "success" if process.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as e:
        execution.stderr = f"Timeout expired after {e.timeout} seconds."
        execution.status = "failed"
    except Exception as e:
        execution.stderr = str(e)
        execution.status = "failed"
    finally:
        execution.finished_at = datetime.datetime.now()
        db.commit()
        db.refresh(execution)
        db.close()

    return execution
