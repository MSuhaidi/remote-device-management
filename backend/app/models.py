from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base
import datetime

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    last_seen = Column(DateTime, default=datetime.datetime.now)
    status = Column(String, default="offline")

    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', status='{self.status}')>"

class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer)
    script_name = Column(String, index=True)
    status = Column(String, default="pending")
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.now)
    finished_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Execution(id={self.id}, script='{self.script_name}', status='{self.status}')>"
