# test_schemas_crud.py
try:
    # Тестируем импорты схем
    from app.schemas.student_goup import (
        StudentCreate, Student, StudentUpdate,
        GroupCreate, Group, GroupUpdate,
        AddStudentToGroup, TransferStudent
    )
    print("✅ Все схемы импортируются корректно")
    
    # Тестируем импорты CRUD
    from app.crud.student_group import (
        create_student, get_student, get_students, update_student, delete_student,
        create_group, get_group, get_groups, update_group, delete_group,
        add_student_to_group, remove_student_from_group, get_students_in_group, transfer_student
    )
    print("✅ Все CRUD функции импортируются корректно")
    
    # Тестируем создание объектов схем
    student_create = StudentCreate(
        first_name="Иван",
        last_name="Петров", 
        email="ivan@example.com"
    )
    print("✅ Схема StudentCreate работает")
    
    group_create = GroupCreate(name="Группа 1")
    print("✅ Схема GroupCreate работает")
    
    print("\n🎉 Все тесты пройдены успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()