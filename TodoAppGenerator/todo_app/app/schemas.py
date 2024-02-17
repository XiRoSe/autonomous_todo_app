from pydantic import BaseModel, Field
from datetime import datetime

class TodoItemBase(BaseModel):
    title: str = Field(...)
    completed: bool = Field(default=False)
    start_time: datetime = Field(default=None)
    end_time: datetime = Field(default=None)

class TodoItemCreate(TodoItemBase):
    pass

class TodoItem(TodoItemCreate):
    id: int = Field(default=None)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "completed": False,
                "start_time": "2022-05-01T12:00:00",
                "end_time": "2022-05-01T14:00:00",
                "id": 1
            }
        }