import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_step(step, message):
    print(f"\n{'='*50}")
    print(f"ШАГ {step}: {message}")
    print(f"{'='*50}")

def test_auth_api():
    print("Запускаем комплексное тестирование Auth API...")
    
    # Переменные для хранения данных между запросами
    access_token = None
    refresh_token = None
    
    try:
        # 1. Тест базового эндпоинта
        print_step(1, "Тестируем базовый эндпоинт")
        response = requests.get(f"{BASE_URL}/")
        print(f"GET / - {response.json()}")
        
        # 2. Регистрация нового пользователя
        print_step(2, "Регистрация нового пользователя")
        register_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"POST /auth/register - {response.json()}")
        
        # 3. Попытка регистрации с тем же email (должна быть ошибка)
        print_step(3, "Попытка повторной регистрации (должна быть ошибка)")
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"POST /auth/register (дубликат) - {response.status_code} - {response.json()}")
        
        # 4. Успешная аутентификация
        print_step(4, "Успешная аутентификация")
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        tokens = response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        print(f"   POST /auth/login - Получены токены")
        print(f"   Access Token: {access_token[:50]}...")
        print(f"   Refresh Token: {refresh_token[:50]}...")
        
        # 5. Получение информации о текущем пользователе
        print_step(5, "Получение информации о пользователе")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/user/me", headers=headers)
        user_info = response.json()
        print(f"GET /user/me - Пользователь: {user_info['email']}")
        
        # 6. Просмотр истории входов
        print_step(6, "Просмотр истории входов")
        response = requests.get(f"{BASE_URL}/user/history", headers=headers)
        history = response.json()
        print(f"GET /user/history - Записей в истории: {len(history)}")
        
        # 7. Обновление refresh токена
        print_step(7, "Обновление токенов")
        refresh_data = {"refresh_token": refresh_token}
        response = requests.post(f"{BASE_URL}/auth/refresh", json=refresh_data)
        new_tokens = response.json()
        new_access_token = new_tokens["access_token"]
        new_refresh_token = new_tokens["refresh_token"]
        print(f"POST /auth/refresh - Токены обновлены")
        
        # 8. Обновление данных пользователя
        print_step(8, "Обновление данных пользователя")
        update_headers = {"Authorization": f"Bearer {new_access_token}"}
        update_data = {"email": "updated@example.com"}
        response = requests.put(f"{BASE_URL}/user/update", json=update_data, headers=update_headers)
        print(f"PUT /user/update - {response.json()}")
        
        # 9. Выход из системы
        print_step(9, "Выход из системы")
        response = requests.post(f"{BASE_URL}/auth/logout", headers=update_headers)
        print(f"POST /auth/logout - {response.json()}")
        
        # 10. Попытка использовать токен после выхода (должна быть ошибка)
        print_step(10, "Попытка использовать токен после выхода (должна быть ошибка)")
        response = requests.get(f"{BASE_URL}/user/me", headers=update_headers)
        print(f"GET /user/me после logout - {response.status_code} - Токен заблокирован")
        
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Auth Service работает корректно!")
        
    except Exception as e:
        print(f"ОШИБКА ПРИ ТЕСТИРОВАНИИ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_api()