# app/api/endpoints/students.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.models.student_group import Student
from app.schemas.student_goup import (
    StudentCreate, Student, StudentUpdate, StudentWithGroup,
    AddStudentToGroup, Message
)
from app.crud.student_group import (
    create_student, get_student, get_students, update_student, delete_student,
    add_student_to_group, remove_student_from_group
)

# Создаем роутер для студентов
router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_new_student(
    student: StudentCreate,
    db: Session = Depends(get_session)
):
    """
    Создать нового студента
    """
    try:
        return create_student(db=db, student=student)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Student])
def read_students(
    skip: int = 0,
    limit: int = 100,
    group_id: int = None,
    db: Session = Depends(get_session)
):
    """
    Получить список студентов
    - **skip**: количество записей для пропуска (пагинация)
    - **limit**: максимальное количество записей для возврата
    - **group_id**: фильтр по ID группы (опционально)
    """
    return get_students(db=db, skip=skip, limit=limit, group_id=group_id)

@router.get("/{student_id}", response_model=Student)
def read_student(
    student_id: int,
    db: Session = Depends(get_session)
):
    """
    Получить информацию о студенте по его ID
    """
    db_student = get_student(db=db, student_id=student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )
    return db_student

@router.put("/{student_id}", response_model=Student)
def update_student_info(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_session)
):
    """
    Обновить информацию о студенте
    """
    db_student = update_student(db=db, student_id=student_id, student_update=student_update)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )
    return db_student

@router.delete("/{student_id}", response_model=Message)
def delete_student_by_id(
    student_id: int,
    db: Session = Depends(get_session)
):
    """
    Удалить студента
    """
    success = delete_student(db=db, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )
    return Message(message="Студент успешно удален")

@router.post("/add-to-group", response_model=Student)
def add_student_to_group_endpoint(
    data: AddStudentToGroup,
    db: Session = Depends(get_session)
):
    """
    Добавить студента в группу
    """
    db_student = add_student_to_group(
        db=db, 
        student_id=data.student_id, 
        group_id=data.group_id
    )
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент или группа не найдены"
        )
    return db_student

@router.post("/{student_id}/remove-from-group", response_model=Student)
def remove_student_from_group_endpoint(
    student_id: int,
    db: Session = Depends(get_session)
):
    """
    Удалить студента из группы
    """
    db_student = remove_student_from_group(db=db, student_id=student_id)
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )
    return db_student