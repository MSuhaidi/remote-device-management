from sqlalchemy import Column, Integer, String, DateTime
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
