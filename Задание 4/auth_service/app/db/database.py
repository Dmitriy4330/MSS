from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем строку подключения к PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в переменных окружения")

print(f"Подключаемся к базе данных: {DATABASE_URL}")

# Создаем движок для подключения к БД
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    print("Создаем таблицы в базе данных...")
    SQLModel.metadata.create_all(engine)
    print("Таблицы успешно созданы!")

def get_session():
    with Session(engine) as session:
        yield session