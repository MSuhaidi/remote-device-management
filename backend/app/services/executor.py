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

# The agent will be responsible for picking up and running scripts.
# This file will be used by the agent's executor in the future.
