# app/main.py
from fastapi import FastAPI
from app.db.database import create_db_and_tables
from contextlib import asynccontextmanager

# Импортируем роутеры
from app.api.endpoints import students, groups

# Функция для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске приложения создаем таблицы в БД
    create_db_and_tables()
    print("Таблицы в базе данных созданы")
    yield
    # При завершении работы приложения можно добавить cleanup логику
    print("Приложение завершает работу")

# Создаем экземпляр FastAPI с lifespan менеджером
app = FastAPI(
    title="Students API",
    description="API для управления студентами и группами",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(students.router)
app.include_router(groups.router)

# Базовый эндпоинт для проверки работы
@app.get("/")
def read_root():
    return {"message": "Students API работает!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API работает корректно"}