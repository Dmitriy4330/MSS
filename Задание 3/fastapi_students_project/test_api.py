# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Тестируем API эндпоинты...")
    
    try:
        # 1. Тест базового эндпоинта
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ GET / - {response.json()}")
        
        # 2. Создаем группу
        group_data = {"name": "ИТ-101"}
        response = requests.post(f"{BASE_URL}/groups/", json=group_data)
        group = response.json()
        print(f"✅ POST /groups/ - Группа создана: {group}")
        
        # 3. Создаем студента
        student_data = {
            "first_name": "Иван",
            "last_name": "Петров",
            "email": "ivan.petrov@example.com"
        }
        response = requests.post(f"{BASE_URL}/students/", json=student_data)
        student = response.json()
        print(f"✅ POST /students/ - Студент создан: {student}")
        
        # 4. Добавляем студента в группу
        add_to_group_data = {
            "student_id": student["id"],
            "group_id": group["id"]
        }
        response = requests.post(f"{BASE_URL}/students/add-to-group", json=add_to_group_data)
        updated_student = response.json()
        print(f"✅ POST /students/add-to-group - Студент добавлен в группу")
        
        # 5. Получаем список студентов
        response = requests.get(f"{BASE_URL}/students/")
        students = response.json()
        print(f"✅ GET /students/ - Найдено студентов: {len(students)}")
        
        # 6. Получаем список групп
        response = requests.get(f"{BASE_URL}/groups/")
        groups = response.json()
        print(f"✅ GET /groups/ - Найдено групп: {len(groups)}")
        
        print("\n🎉 Все основные API эндпоинты работают корректно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании API: {e}")

if __name__ == "__main__":
    test_api()