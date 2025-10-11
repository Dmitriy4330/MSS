import redis
import os
from dotenv import load_dotenv
import json
from typing import Optional

load_dotenv()

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Создаем клиент Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

def add_to_blacklist(token: str, expire_time: int) -> bool:
    """Добавляет токен в черный список Redis"""
    try:
        # Сохраняем токен с временем истечения (в секундах)
        redis_client.setex(f"blacklist:{token}", expire_time, "true")
        return True
    except Exception:
        return False

def is_token_blacklisted(token: str) -> bool:
    """Проверяет, находится ли токен в черном списке"""
    try:
        return redis_client.exists(f"blacklist:{token}") == 1
    except Exception:
        return False

def test_redis_connection():
    """Тестирует подключение к Redis"""
    try:
        redis_client.ping()
        print("Подключение к Redis установлено")
        return True
    except Exception as e:
        print(f"Ошибка подключения к Redis: {e}")
        return False