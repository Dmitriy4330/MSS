**Auth Service**


1. **Клонирование и настройка**

    ```bash
    # Создание виртуального окружения
    python -m venv venv

    # Активация окружения
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

    # Установка зависимостей
    pip install -r requirements.txt

2. **Настройка окружения**
    Скопируйте .env.example в .env и настройте параметры:

3. **Запуск сервисов**
    Запуск базы данных и Redis
    docker compose up -d

    Запуск приложения
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. **ДОП документы**
    Можно глянуть документацию
    http://localhost:8000/docs
    http://localhost:8000/redoc

5. **Эндпоинты**
    POST	/auth/register	Регистрация нового пользователя
    POST	/auth/login	    Аутентификация и получение токенов
    POST	/auth/refresh	Обновление access токена
    POST	/auth/logout	Выход из системы
    GET	    /user/me	    Информация о текущем пользователе	
    PUT	    /user/update	Обновление данных пользователя	
    GET	    /user/history	История входов пользователя