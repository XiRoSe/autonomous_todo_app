import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
from sqlalchemy.orm import validates


class TodoItem(Base):
    __tablename__ = "todo_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    @validates('title')
    def validate_title(self, key, title):
        assert isinstance(title, str), f"{key} must be of 'str' type"
        return title

    @validates('start_time', 'end_time')
    def validate_time(self, key, time):
        assert isinstance(time, datetime.datetime), f"{key} must be of 'datetime' type"
        return time

    def __repr__(self):
        safe_title = repr(self.title) if self.title else ''
        return f"<TodoItem(id='{self.id}', title={safe_title}, completed='{self.completed}', start_time='{self.start_time}', end_time='{self.end_time}')>"
