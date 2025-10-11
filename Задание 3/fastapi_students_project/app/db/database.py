# app/db/database.py
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем строку подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем "движок" для подключения к базе данных
# echo=True включает вывод SQL-запросов в консоль (удобно для отладки)
engine = create_engine(DATABASE_URL, echo=True)

# Функция для создания таблиц в базе данных
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Функция для получения сессии базы данных (будем использовать в зависимостях FastAPI)
def get_session():
    with Session(engine) as session:
        yield session