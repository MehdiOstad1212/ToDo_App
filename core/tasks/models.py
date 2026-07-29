from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from core.database import Base
import datetime

class TaskModel (Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, autoincrement = True)
    title = Column(String(150), nullable = False)
    description = Column(String(500), default = True)
    is_completed = Column(Boolean, default = False)
    created_at = Column(DateTime(), server_default = func.now())
    updated_at = Column(DateTime(), server_default = func.now(),
                        server_onupdate = func.now())