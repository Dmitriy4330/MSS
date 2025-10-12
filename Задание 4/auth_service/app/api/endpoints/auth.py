from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session
from datetime import timedelta

from app.db.database import get_session
from app.schemas.user import (
    UserRegister, UserLogin, Token, TokenRefresh, 
    Message, LoginHistoryCreate
)
from app.core.security import (
    create_access_token, create_refresh_token, verify_token,
    verify_password, get_password_hash
)
from app.core.redis_client import add_to_blacklist, is_token_blacklisted
from app.crud.user import (
    create_user, get_user_by_email, authenticate_user,
    create_login_history, get_user_login_history
)
from app.core.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=Message, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_session)
):
    """
    Регистрация нового пользователя
    """
    try:
        # Создаем пользователя
        user = create_user(db=db, user=user_data)
        
        # Создаем запись в истории входов
        history_data = LoginHistoryCreate(
            user_id=user.id,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None
        )
        create_login_history(db=db, history=history_data)
        
        return Message(message="Пользователь успешно зарегистрирован")
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_session)
):
    """
    Аутентификация пользователя и выдача токенов
    """
    # Аутентифицируем пользователя
    user = authenticate_user(db=db, email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем запись в истории входов
    history_data = LoginHistoryCreate(
        user_id=user.id,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None
    )
    create_login_history(db=db, history=history_data)
    
    # Создаем токены
    token_data = {"user_id": user.id, "email": user.email}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post("/refresh", response_model=Token)
def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_session)
):
    """
    Обновление access токена с помощью refresh токена
    """
    refresh_token = token_data.refresh_token
    
    # Проверяем, не в черном списке ли refresh токен
    if is_token_blacklisted(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh токен недействителен"
        )
    
    # Проверяем и декодируем refresh токен
    payload = verify_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh токен"
        )
    
    user_id = payload.get("user_id")
    email = payload.get("email")
    
    if user_id is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh токен"
        )
    
    # Проверяем, существует ли пользователь
    user = get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    # Добавляем старый refresh токен в черный список
    from app.core.security import REFRESH_TOKEN_EXPIRE_DAYS
    refresh_token_expire_seconds = REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    add_to_blacklist(refresh_token, refresh_token_expire_seconds)
    
    # Создаем новые токены
    token_data = {"user_id": user.id, "email": user.email}
    access_token = create_access_token(data=token_data)
    new_refresh_token = create_refresh_token(data=token_data)
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

@router.post("/logout", response_model=Message)
def logout(
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Выход из системы - добавление токена в черный список
    """
    # Получаем токен из заголовка Authorization
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        
        # Добавляем access токен в черный список
        from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
        access_token_expire_seconds = ACCESS_TOKEN_EXPIRE_MINUTES * 60
        add_to_blacklist(token, access_token_expire_seconds)
    
    return Message(message="Успешный выход из системы")