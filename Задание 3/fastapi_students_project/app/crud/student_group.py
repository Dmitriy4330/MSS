# app/crud/student_group.py
from sqlmodel import Session, select, func
from typing import List, Optional
from app.models.student_group import Student, Group
from app.schemas.student_goup import StudentCreate, StudentUpdate, GroupCreate, GroupUpdate 

# ========== STUDENT CRUD OPERATIONS ==========

def create_student(db: Session, student: StudentCreate) -> Student:
    """
    Создать нового студента
    """
    # Проверяем, нет ли студента с таким email
    existing_student = db.exec(
        select(Student).where(Student.email == student.email)
    ).first()
    
    if existing_student:
        raise ValueError(f"Студент с email {student.email} уже существует")
    
    # Создаем объект студента для базы данных
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        email=student.email
    )
    
    # Добавляем в базу и сохраняем
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student

def get_student(db: Session, student_id: int) -> Optional[Student]:
    """
    Получить студента по ID
    """
    return db.get(Student, student_id)

def get_students(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    group_id: Optional[int] = None
) -> List[Student]:
    """
    Получить список студентов с пагинацией и фильтром по группе
    """
    query = select(Student)
    
    if group_id is not None:
        query = query.where(Student.group_id == group_id)
    
    students = db.exec(
        query.offset(skip).limit(limit)
    ).all()
    
    return students

def update_student(
    db: Session, 
    student_id: int, 
    student_update: StudentUpdate
) -> Optional[Student]:
    """
    Обновить информацию о студенте
    """
    db_student = db.get(Student, student_id)
    if not db_student:
        return None
    
    # Обновляем только переданные поля
    update_data = student_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student

def delete_student(db: Session, student_id: int) -> bool:
    """
    Удалить студента
    """
    db_student = db.get(Student, student_id)
    if not db_student:
        return False
    
    db.delete(db_student)
    db.commit()
    return True

def add_student_to_group(db: Session, student_id: int, group_id: int) -> Optional[Student]:
    """
    Добавить студента в группу
    """
    student = db.get(Student, student_id)
    group = db.get(Group, group_id)
    
    if not student or not group:
        return None
    
    student.group_id = group_id
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student

def remove_student_from_group(db: Session, student_id: int) -> Optional[Student]:
    """
    Удалить студента из группы
    """
    student = db.get(Student, student_id)
    if not student:
        return None
    
    student.group_id = None
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student

# ========== GROUP CRUD OPERATIONS ==========

def create_group(db: Session, group: GroupCreate) -> Group:
    """
    Создать новую группу
    """
    # Проверяем, нет ли группы с таким именем
    existing_group = db.exec(
        select(Group).where(Group.name == group.name)
    ).first()
    
    if existing_group:
        raise ValueError(f"Группа с именем {group.name} уже существует")
    
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group

def get_group(db: Session, group_id: int) -> Optional[Group]:
    """
    Получить группу по ID
    """
    return db.get(Group, group_id)

def get_groups(db: Session, skip: int = 0, limit: int = 100) -> List[Group]:
    """
    Получить список групп с пагинацией
    """
    groups = db.exec(
        select(Group).offset(skip).limit(limit)
    ).all()
    
    return groups

def update_group(
    db: Session, 
    group_id: int, 
    group_update: GroupUpdate
) -> Optional[Group]:
    """
    Обновить информацию о группе
    """
    db_group = db.get(Group, group_id)
    if not db_group:
        return None
    
    update_data = group_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_group, field, value)
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group

def delete_group(db: Session, group_id: int) -> bool:
    """
    Удалить группу
    """
    db_group = db.get(Group, group_id)
    if not db_group:
        return False
    
    # Убираем связь у студентов этой группы
    students_in_group = db.exec(
        select(Student).where(Student.group_id == group_id)
    ).all()
    
    for student in students_in_group:
        student.group_id = None
        db.add(student)
    
    db.delete(db_group)
    db.commit()
    return True

def get_students_in_group(db: Session, group_id: int) -> List[Student]:
    """
    Получить всех студентов в группе
    """
    students = db.exec(
        select(Student).where(Student.group_id == group_id)
    ).all()
    
    return students

def transfer_student(
    db: Session, 
    student_id: int, 
    from_group_id: int, 
    to_group_id: int
) -> Optional[Student]:
    """
    Перевести студента из одной группы в другую
    """
    student = db.get(Student, student_id)
    from_group = db.get(Group, from_group_id)
    to_group = db.get(Group, to_group_id)
    
    # Проверяем, что все объекты существуют
    if not student or not from_group or not to_group:
        return None
    
    # Проверяем, что студент действительно в исходной группе
    if student.group_id != from_group_id:
        raise ValueError("Студент не находится в указанной исходной группе")
    
    student.group_id = to_group_id
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student