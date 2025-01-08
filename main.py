from http.client import HTTPException
from fastapi import FastAPI, Request, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from .database import User, Item, get_db  # Модели пользователя и товаров
from .routers.items import items_router
from .routers.users import user_router, verify_password

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Подключение роутеров
app.include_router(user_router)
app.include_router(items_router)

# CryptContext для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хэширует пароль."""
    return pwd_context.hash(password)


# Главная страница
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Страница входа
@app.get("/login/")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Страница выхода
@app.get("/logout/")
def logout_form(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})


# Страница оплаты
@app.get("/pay/")
def payment_page(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})


# Регистрация
@app.post("/register")
def register(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db),
        request: Request = None,
):
    # Проверяем, существует ли пользователь с таким именем
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь с таким именем уже существует"
        })

    # Хешируем пароль
    hashed_password = get_password_hash(password)

    # Создаем нового пользователя
    new_user = User(username=username, hashed_password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()  # Откатываем изменения, если произошла ошибка
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": f"Ошибка при регистрации пользователя: {str(e)}"
        })

    # Редирект на страницу входа после успешной регистрации
    return RedirectResponse("/login/", status_code=303)


# Страница с информацией о пользователе
@app.get("/user-info/")
def get_user_info(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).first()  # Получаем первого пользователя (или используйте сессии для входа)
    return templates.TemplateResponse("user_info.html", {"request": request, "user": user})

# Страница для изменения пароля
@app.get("/edit-password/")
def edit_password_form(request: Request):
    return templates.TemplateResponse("edit_password.html", {"request": request})


@app.post("/edit-password/")
def edit_password(new_password: str = Form(...), db: Session = Depends(get_db)):
    # Получаем пользователя из базы
    user = db.query(User).first()

    # Хешируем новый пароль
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password

    db.commit()
    return RedirectResponse("/user-info/", status_code=303)


# Страница с товарами
@app.get("/items/")
def get_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return templates.TemplateResponse("items_list.html", {"request": request, "items": items})


# Удаление пользователя
@app.post("/delete-user/")
def delete_user(db: Session = Depends(get_db)):
    # Для примера удаляем первого пользователя
    user = db.query(User).first()

    if user:
        db.delete(user)
        db.commit()
        return RedirectResponse("/", status_code=303)
    return {"error": "Пользователь не найден"}