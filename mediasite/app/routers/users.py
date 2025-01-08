from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.database import User
from passlib.context import CryptContext

user_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

# Настраиваем хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль на соответствие хэшу."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширует пароль."""
    return pwd_context.hash(password)


@user_router.post("/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Простая проверка логина и пароля без токенов.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")
    return {"message": f"Добро пожаловать, {user.username}!"}


@user_router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """
    Возвращает список всех пользователей.
    """
    users = db.query(User).all()
    return users

@user_router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создает нового пользователя.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Имя пользователя уже используется")

    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Удаляет пользователя по его ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.delete(user)
    db.commit()
    return user


