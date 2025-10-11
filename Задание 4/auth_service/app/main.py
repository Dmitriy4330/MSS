from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.core.redis_client import test_redis_connection
from contextlib import asynccontextmanager

# Импортируем роутеры
from app.api.endpoints import auth, user

# Функция для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске приложения создаем таблицы в БД
    create_db_and_tables()
    print("Таблицы в базе данных созданы")
    
    # Тестируем подключение к Redis
    test_redis_connection()
    
    yield
    # При завершении работы приложения
    print("Приложение завершает работу")

# Создаем экземпляр FastAPI
app = FastAPI(
    title="Auth Service API",
    description="Сервис аутентификации и авторизации с JWT",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(user.router)

# Базовый эндпоинт для проверки
@app.get("/")
def read_root():
    return {"message": "Auth Service работает!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Auth Service работает корректно"}