# Students API

FastAPI приложение для управления студентами и группами.

## Требования

- Python 3.8+
- Docker и Docker Compose
- PostgreSQL (запускается через Docker)

## Установка и запуск

1. **Клонируйте репозиторий**
2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source .\venv\Scripts\activate
3. **Установите зависимости:**
    pip install -r requirements.txt
4. **Настройте переменные окружения:**
    Скопируйте .env.example в .env
    Настройте параметры подключения к БД
5. **Запустите базу данных:**
    docker compose up -d
6. **Запустите приложение:**
    Запуск из корня проекта(папка fastapi_students_project)
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
7. **После запуска можно глянуть:**
    1) http://localhost:8000/docs
    2) http://localhost:8000/redoc
8. **Основные эндпоинты:**
    POST /students/ - Создать студента
    GET /students/ - Получить список студентов
    GET /students/{id} - Получить студента по ID
    PUT /students/{id} - Обновить студента
    DELETE /students/{id} - Удалить студента
    POST /students/add-to-group - Добавить студента в группу
    POST /students/{id}/remove-from-group - Удалить студента из группы
9. **Группы:**
    POST /groups/ - Создать группу
    GET /groups/ - Получить список групп
    GET /groups/{id} - Получить группу по ID
    PUT /groups/{id} - Обновить группу
    DELETE /groups/{id} - Удалить группу
    GET /groups/{id}/students - Получить студентов группы
    POST /groups/transfer-student - Перевести студента между группами
