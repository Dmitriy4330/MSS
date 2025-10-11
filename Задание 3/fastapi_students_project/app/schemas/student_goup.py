# app/schemas/student_group.py
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# ========== SCHEMAS FOR STUDENTS ==========

# Базовая схема студента (общие поля)
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

# Схема для создания студента (без ID)
class StudentCreate(StudentBase):
    pass

# Схема для обновления студента (все поля опциональны)
class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    group_id: Optional[int] = None

# Схема студента в ответе API (с ID и датами)
class Student(StudentBase):
    id: int
    group_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True  # Работает с ORM моделями

# Схема студента с информацией о группе
class StudentWithGroup(Student):
    group_name: Optional[str] = None

# ========== SCHEMAS FOR GROUPS ==========

# Базовая схема группы
class GroupBase(BaseModel):
    name: str

# Схема для создания группы
class GroupCreate(GroupBase):
    pass

# Схема для обновления группы
class GroupUpdate(BaseModel):
    name: Optional[str] = None

# Схема группы в ответе API
class Group(GroupBase):
    id: int
    created_at: datetime
    student_count: int = 0  # Количество студентов в группе
    
    class Config:
        from_attributes = True

# Схема группы со списком студентов
class GroupWithStudents(Group):
    students: List[Student] = []

# ========== SPECIAL SCHEMAS ==========

# Схема для добавления студента в группу
class AddStudentToGroup(BaseModel):
    student_id: int
    group_id: int

# Схема для перевода студента между группами
class TransferStudent(BaseModel):
    student_id: int
    from_group_id: int
    to_group_id: int

# Схема ответа с сообщением
class Message(BaseModel):
    message: str