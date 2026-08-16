from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    func,
    ForeignKey,
)
from core.database import Base
from sqlalchemy.orm import relationship
import datetime


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(
        DateTime(), server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("UserModel", back_populates="tasks", uselist=False)
