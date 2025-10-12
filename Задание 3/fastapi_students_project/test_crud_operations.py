# test_crud_operations.py
from app.db.database import get_session
from app.crud.student_group import create_student, create_group, get_students, get_groups
from app.schemas.student_goup import StudentCreate, GroupCreate

def test_crud_operations():
    print("🧪 Тестируем CRUD операции...")
    
    # Используем контекстный менеджер для сессии
    from app.db.database import engine
    from sqlmodel import Session
    
    with Session(engine) as db:
        try:
            # Тест создания группы
            group_data = GroupCreate(name="Тестовая группа")
            group = create_group(db, group_data)
            print(f"✅ Группа создана: ID={group.id}, Name={group.name}")
            
            # Тест создания студента
            student_data = StudentCreate(
                first_name="Тестовый",
                last_name="Студент",
                email="test@example.com"
            )
            student = create_student(db, student_data)
            print(f"✅ Студент создан: ID={student.id}, Name={student.first_name} {student.last_name}")
            
            # Тест получения списков
            groups = get_groups(db)
            students = get_students(db)
            
            print(f"✅ Группы в базе: {len(groups)}")
            print(f"✅ Студенты в базе: {len(students)}")
            
            print("\n🎉 CRUD операции работают корректно!")
            
        except Exception as e:
            print(f"❌ Ошибка при тестировании CRUD: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_crud_operations()