from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    due_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_done = Column(Boolean, default=False)
