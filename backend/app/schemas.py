from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceCreate(BaseModel):
    name: str

class Heartbeat(BaseModel):
    device_id: int

class DeviceOut(BaseModel):
    id: int
    name: str
    last_seen: datetime
    status: str

    class Config:
        from_attributes = True

class ScriptRunRequest(BaseModel):
    script_name: str

class ScriptRunResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

class ExecutionOut(BaseModel):
    id: int
    script_name: str
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True
