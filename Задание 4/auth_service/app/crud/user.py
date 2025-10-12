from sqlmodel import Session, select
from typing import Optional, List
from app.models.user import User, LoginHistory
from app.schemas.user import UserCreate, UserUpdate, LoginHistoryCreate
from app.core.security import get_password_hash, verify_password
from datetime import datetime


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Получить пользователя по email"""
    return db.exec(select(User).where(User.email == email)).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Получить пользователя по ID"""
    return db.get(User, user_id)

def create_user(db: Session, user: UserCreate) -> User:
    """Создать нового пользователя"""
    # Проверяем, нет ли пользователя с таким email
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Пользователь с таким email уже существует")
    
    # Хешируем пароль
    hashed_password = get_password_hash(user.password)
    
    # Создаем пользователя
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Аутентификация пользователя по email и паролю"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Обновить данные пользователя"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    # Обновляем только переданные поля
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "email" in update_data:
        # Проверяем, что новый email не занят другим пользователем
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user and existing_user.id != user_id:
            raise ValueError("Пользователь с таким email уже существует")
        db_user.email = update_data["email"]
    
    if "password" in update_data:
        db_user.hashed_password = get_password_hash(update_data["password"])
    
    db_user.updated_at = datetime.utcnow()
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


def create_login_history(db: Session, history: LoginHistoryCreate) -> LoginHistory:
    """Создать запись в истории входов"""
    db_history = LoginHistory(
        user_id=history.user_id,
        user_agent=history.user_agent,
        ip_address=history.ip_address
    )
    
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    
    return db_history

def get_user_login_history(db: Session, user_id: int, limit: int = 10) -> List[LoginHistory]:
    """Получить историю входов пользователя"""
    return db.exec(
        select(LoginHistory)
        .where(LoginHistory.user_id == user_id)
        .order_by(LoginHistory.login_time.desc())
        .limit(limit)
    ).all()