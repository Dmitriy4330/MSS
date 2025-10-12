# app/models/student_group.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime

class Group(SQLModel, table=True):
    # Поля таблицы
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    
    # Связь "один ко многим" с Student
    students: List["Student"] = Relationship(back_populates="group")

class Student(SQLModel, table=True):
    # Поля таблицы
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(index=True, max_length=100)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    
    # Внешний ключ для связи с Group
    group_id: Optional[int] = Field(default=None, foreign_key="group.id")
    
    # Связь "многие к одному" с Group
    group: Optional[Group] = Relationship(back_populates="students")