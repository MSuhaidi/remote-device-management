from pydantic import BaseModel
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str

class DeviceOut(BaseModel):
    id: int
    name: str
    last_seen: datetime
    status: str

    class Config:
        from_attributes = True
