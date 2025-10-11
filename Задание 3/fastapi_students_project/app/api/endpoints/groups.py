# app/api/endpoints/groups.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.models.student_group import Group, Student
from app.schemas.student_goup import (
    GroupCreate, Group, GroupUpdate, GroupWithStudents,
    TransferStudent, Message
)
from app.crud.student_group import (
    create_group, get_group, get_groups, update_group, delete_group,
    get_students_in_group, transfer_student
)

# Создаем роутер для групп
router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=Group, status_code=status.HTTP_201_CREATED)
def create_new_group(
    group: GroupCreate,
    db: Session = Depends(get_session)
):
    """
    Создать новую группу
    """
    try:
        return create_group(db=db, group=group)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Group])
def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    """
    Получить список групп
    - **skip**: количество записей для пропуска (пагинация)
    - **limit**: максимальное количество записей для возврата
    """
    return get_groups(db=db, skip=skip, limit=limit)

@router.get("/{group_id}", response_model=Group)
def read_group(
    group_id: int,
    db: Session = Depends(get_session)
):
    """
    Получить информацию о группе по ее ID
    """
    db_group = get_group(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    return db_group

@router.put("/{group_id}", response_model=Group)
def update_group_info(
    group_id: int,
    group_update: GroupUpdate,
    db: Session = Depends(get_session)
):
    """
    Обновить информацию о группе
    """
    db_group = update_group(db=db, group_id=group_id, group_update=group_update)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    return db_group

@router.delete("/{group_id}", response_model=Message)
def delete_group_by_id(
    group_id: int,
    db: Session = Depends(get_session)
):
    """
    Удалить группу
    """
    success = delete_group(db=db, group_id=group_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    return Message(message="Группа успешно удалена")

@router.get("/{group_id}/students", response_model=List[Student])
def get_students_in_group_endpoint(
    group_id: int,
    db: Session = Depends(get_session)
):
    """
    Получить всех студентов в группе
    """
    # Сначала проверяем, существует ли группа
    group = get_group(db=db, group_id=group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    
    return get_students_in_group(db=db, group_id=group_id)

@router.post("/transfer-student", response_model=Student)
def transfer_student_between_groups(
    data: TransferStudent,
    db: Session = Depends(get_session)
):
    """
    Перевести студента из группы A в группу B
    """
    try:
        db_student = transfer_student(
            db=db,
            student_id=data.student_id,
            from_group_id=data.from_group_id,
            to_group_id=data.to_group_id
        )
        if not db_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студент или группы не найдены"
            )
        return db_student
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )