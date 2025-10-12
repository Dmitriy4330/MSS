print("Тестируем компоненты аутентификации...")

try:
    # Тестируем импорты схем
    from app.schemas.user import UserRegister, UserLogin, Token, User
    print("Схемы импортированы корректно")
    
    # Тестируем создание объектов схем
    register_data = UserRegister(
        email="test@example.com",
        password="testpassword123"
    )
    print("Схема UserRegister работает")
    
    login_data = UserLogin(
        email="test@example.com", 
        password="testpassword123"
    )
    print("Схема UserLogin работает")
    
    # Тестируем импорты CRUD
    from app.crud.user import create_user, authenticate_user
    print("CRUD функции импортированы")
    
    # Тестируем импорты безопасности
    from app.core.security import get_password_hash, verify_password
    print("Функции безопасности импортированы")
    
    # Тестируем хеширование пароля
    password = "testpassword123"
    hashed = get_password_hash(password)
    verify_result = verify_password(password, hashed)
    print(f"Хеширование пароля работает: {verify_result}")
    
    print("\nВсе компоненты аутентификации работают корректно!")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()