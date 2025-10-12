from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserRegister(BaseModel):
    """Схема для регистрации пользователя"""
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Схема для токенов"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """Схема для обновления токена"""
    refresh_token: str

class TokenData(BaseModel):
    """Данные внутри JWT токена"""
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str

class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    """Схема пользователя в ответе API"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class LoginHistoryBase(BaseModel):
    """Базовая схема истории входов"""
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None

class LoginHistoryCreate(LoginHistoryBase):
    """Схема для создания записи истории входа"""
    user_id: int

class LoginHistory(LoginHistoryBase):
    """Схема истории входов в ответе API"""
    id: int
    user_id: int
    login_time: datetime
    
    class Config:
        from_attributes = True


class Message(BaseModel):
    """Схема для сообщений"""
    message: str

class UserWithHistory(User):
    """Пользователь с историей входов"""
    login_history: List[LoginHistory] = []