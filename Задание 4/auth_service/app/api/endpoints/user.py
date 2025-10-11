from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.schemas.user import (
    User, UserUpdate, LoginHistory, Message
)
from app.core.auth import get_current_active_user
from app.crud.user import (
    update_user, get_user_login_history, get_user_by_id
)

router = APIRouter(prefix="/user", tags=["user"])

@router.put("/update", response_model=Message)
def update_user_info(
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Обновление данных пользователя (email или пароль)
    """
    try:
        updated_user = update_user(
            db=db, 
            user_id=current_user.user_id, 
            user_update=user_update
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        
        return Message(message="Данные пользователя успешно обновлены")
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/history", response_model=List[LoginHistory])
def get_login_history(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_session),
    limit: int = 10
):
    """
    Просмотр истории входов пользователя
    """
    history = get_user_login_history(
        db=db, 
        user_id=current_user.user_id, 
        limit=limit
    )
    return history

@router.get("/me", response_model=User)
def get_current_user_info(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Получение информации о текущем пользователе
    """
    user = get_user_by_id(db=db, user_id=current_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user