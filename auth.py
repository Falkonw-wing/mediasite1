# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
# from app.database import User
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
#
# # Настройка контекста хэширования
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# # Конфигурация JWT
# SECRET_KEY = "your_secret_key"  # Измените на более сложный ключ
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# def create_access_token(data: dict):
#     """Создает JWT токен."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# def decode_access_token(token: str):
#     """Декодирует JWT токен."""
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None
#
# def verify_password(plain_password, hashed_password):
#     """Проверяет соответствие пароля хэшу."""
#     return pwd_context.verify(plain_password, hashed_password)
#
# def get_password_hash(password):
#     """Хэширует пароль."""
#     return pwd_context.hash(password)
#
# def authenticate_user(db: Session, username: str, password: str):
#     """Проверяет пользователя и пароль."""
#     user = db.query(User).filter(User.username == username).first()
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user
