from pydantic import BaseModel
from datetime import date

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        from_attributes = True
