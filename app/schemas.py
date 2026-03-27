from pydantic import BaseModel
from typing import Optional
from datetime import date

# Todo作成用
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    due_date: Optional[date] = None
    completed: bool = False

# Todo更新用
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None

# Todoレスポンス用
class Todo(BaseModel):
    id: int
    title: str
    description: str
    due_date: Optional[date]
    completed: bool

    class Config:
        from_attributes = True  # Pydantic V2: orm_modeの代替
