# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# def verify_password(plain_password, hashed_password):
#     """Проверка пароля."""
#     return pwd_context.verify(plain_password, hashed_password)
#
# def get_password_hash(password):
#     """Хеширование пароля."""
#     return pwd_context.hash(password)
#
# def create_access_token(data: dict):
#     """Создание токена доступа."""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
