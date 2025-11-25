# 🔐 Модуль Auth (Аутентификация)

> **Часть проекта:** Ansar Store - Интернет-магазин  
> **Назначение:** JWT аутентификация и безопасность доступа

---

## 📌 Контекст проекта

Модуль Auth - это служба безопасности всей системы. Отвечает за вход, выход, токены доступа. Работает напрямую с Users (данные пользователей) и защищает все остальные модули через JWT токены.

**Роль в системе:** Обеспечить безопасный доступ к системе только авторизованным пользователям.

---

## ✅ Текущий статус: 40%

**Что работает:**
- ✅ Хеширование паролей (bcrypt)
- ✅ Функции hash_password, verify_password

**Что требует реализации:**
- ⚠️ JWT токены (создание, проверка)
- ⚠️ Эндпоинты register, login
- ⚠️ Refresh токены
- ⚠️ Сброс пароля
- ⚠️ Email подтверждение

---

## 🎯 Цель модуля

**После полной реализации система будет:**
1. Безопасно регистрировать новых пользователей
2. Проверять credentials при входе
3. Выдавать JWT токены для доступа к API
4. Обновлять токены через refresh
5. Восстанавливать пароль через email
6. Подтверждать email при регистрации
7. Поддерживать OAuth (Google, Facebook)
8. Включать 2FA для дополнительной безопасности

---

## 📊 Структура модуля

```
auth/
├── services.py   # Хеширование паролей, JWT функции
├── routers.py    # ⚠️ API эндпоинты (ЗАГЛУШКА!)
└── schemas.py    # ⚠️ Pydantic схемы (ПУСТО!)
```

---

## 📝 Техническое задание

### 1. JWT Токены (КРИТИЧНО!)
**Задача:** Реализовать создание и проверку JWT токенов

**Где реализовать:** `services.py`

**Что нужно:**

**Конфигурация (добавить в .env):**
```bash
SECRET_KEY=<случайная строка 64 символа>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Создание access токена:**
```python
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "получить из .env"
ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    """
    Создать access токен
    
    1. Подготовить данные: {"sub": str(user_id)}
    2. Добавить exp (срок действия): datetime.utcnow() + 30 минут
    3. Закодировать: jwt.encode(data, SECRET_KEY, ALGORITHM)
    4. Вернуть токен
    """
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "type": "access"
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
```

**Создание refresh токена:**
```python
def create_refresh_token(user_id: int) -> str:
    """
    Аналогично access, но:
    - exp: 7 дней
    - type: "refresh"
    """
    data = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "refresh"
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
```

**Проверка токена:**
```python
from jose import JWTError
from fastapi import HTTPException

def verify_token(token: str) -> dict:
    """
    Проверить и декодировать токен
    
    1. Попытаться декодировать: jwt.decode(token, SECRET_KEY, ALGORITHM)
    2. Если ошибка → HTTPException(401, "Invalid token")
    3. Вернуть payload с user_id
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Недействительный или истекший токен"
        )
```

---

### 2. Pydantic схемы (КРИТИЧНО!)
**Задача:** Создать схемы валидации

**Где реализовать:** Создать файл `schemas.py`

```python
from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    """Регистрация нового пользователя"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)
    phone: str | None = None

class UserLogin(BaseModel):
    """Вход пользователя"""
    username: str
    password: str

class Token(BaseModel):
    """Ответ с токенами"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    """Запрос обновления токена"""
    refresh_token: str
```

---

### 3. Эндпоинт Register (КРИТИЧНО!)
**Задача:** Регистрация нового пользователя

**Где реализовать:** `routers.py`

```python
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from modules.users import crud as user_crud
from modules.users.models import UserRole
from . import services, schemas

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.Token)
async def register(
    user_data: schemas.UserRegister,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Регистрация пользователя
    
    Шаги:
    1. Проверить, не существует ли username
    2. Проверить, не существует ли email
    3. Захешировать пароль (services.hash_password)
    4. Создать пользователя (user_crud.create_user)
    5. Создать токены (services.create_access_token/refresh_token)
    6. Вернуть токены
    """
    # Проверка username
    existing = await user_crud.get_user_by_username(db, user_data.username)
    if existing:
        raise HTTPException(400, "Username уже занят")
    
    # Проверка email
    existing = await user_crud.get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(400, "Email уже используется")
    
    # Хеширование пароля
    hashed = services.hash_password(user_data.password)
    
    # Создание пользователя
    user = await user_crud.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=hashed,
        phone=user_data.phone,
        role=UserRole.USER
    )
    
    # Создание токенов
    access_token = services.create_access_token(user.id)
    refresh_token = services.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

---

### 4. Эндпоинт Login (КРИТИЧНО!)
**Задача:** Вход пользователя

**Где реализовать:** `routers.py`

```python
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Вход пользователя
    
    Шаги:
    1. Найти пользователя по username
    2. Проверить существование
    3. Проверить пароль (services.verify_password)
    4. Проверить is_active
    5. Создать токены
    6. Вернуть токены
    """
    # Поиск пользователя
    user = await user_crud.get_user_by_username(db, form_data.username)
    
    if not user:
        raise HTTPException(401, "Неверный логин или пароль")
    
    # Проверка пароля
    if not services.verify_password(form_data.password, user.password):
        raise HTTPException(401, "Неверный логин или пароль")
    
    # Проверка активности
    if not user.is_active:
        raise HTTPException(403, "Аккаунт заблокирован")
    
    # Создание токенов
    access_token = services.create_access_token(user.id)
    refresh_token = services.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

---

### 5. Обновление токена (ВАЖНО!)
**Задача:** Refresh токен для продления сессии

**Где реализовать:** `routers.py`

```python
@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    data: schemas.TokenRefresh,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновление access токена
    
    1. Проверить refresh токен (verify_token)
    2. Проверить type == "refresh"
    3. Извлечь user_id
    4. Проверить, что пользователь существует и активен
    5. Создать новые токены
    6. Вернуть новые токены
    """
    # Проверка токена
    payload = services.verify_token(data.refresh_token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(401, "Неверный тип токена")
    
    user_id = int(payload.get("sub"))
    
    # Проверка пользователя
    user = await user_crud.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(401, "Пользователь не найден")
    
    # Новые токены
    access_token = services.create_access_token(user.id)
    refresh_token = services.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

---

### 6. Текущий пользователь (ВАЖНО!)
**Задача:** Получить данные авторизованного пользователя

**Где реализовать:** `services.py`

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from modules.users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Получить текущего пользователя из токена
    
    1. Проверить токен (verify_token)
    2. Извлечь user_id
    3. Получить User из БД
    4. Проверить существование
    5. Вернуть User
    
    Использование:
    @router.get("/me")
    async def me(user: User = Depends(get_current_user)):
        return user
    """
```

---

### 7. Сброс пароля (СРЕДНИЙ ПРИОРИТЕТ)
**Задача:** Восстановление пароля через email

**Что нужно:**

**Создание токена для сброса:**
```python
def create_password_reset_token(email: str) -> str:
    """
    Токен для сброса пароля (срок: 1 час)
    """
    data = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "type": "password_reset"
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
```

**Эндпоинты:**
```python
@router.post("/password-reset-request")
async def request_password_reset(email: str):
    """
    1. Проверить, существует ли пользователь
    2. Создать токен сброса
    3. Отправить email с ссылкой
    4. Вернуть success
    
    Ссылка: https://site.com/reset?token=...
    """

@router.post("/password-reset")
async def reset_password(token: str, new_password: str):
    """
    1. Проверить токен
    2. Извлечь email
    3. Найти пользователя
    4. Обновить пароль (хешированный)
    5. Вернуть success
    """
```

---

## 🔍 Важные детали

### Структура JWT payload
```json
{
  "sub": "123",           // user_id
  "exp": 1234567890,      // срок действия
  "type": "access"        // тип токена
}
```

### Типы токенов
```
access  → Короткий срок (30 мин) → Доступ к API
refresh → Длинный срок (7 дней) → Обновление access
```

### Безопасность
```
✓ Пароли хешируются (bcrypt)
✓ JWT подписываются секретным ключом
✓ Токены имеют срок действия
✓ Refresh токены для продления сессии
✗ Логировать попытки входа (TODO)
✗ Rate limiting (TODO)
✗ Блокировка после N неудач (TODO)
```

---

## 🧪 Тестовые сценарии

1. **Регистрация:**
   - ✓ Успешная регистрация → токены
   - ✗ Дубликат username
   - ✗ Дубликат email
   - ✗ Слабый пароль

2. **Вход:**
   - ✓ Правильные credentials → токены
   - ✗ Неправильный пароль
   - ✗ Несуществующий пользователь
   - ✗ Заблокированный аккаунт

3. **Refresh:**
   - ✓ Валидный refresh токен → новые токены
   - ✗ Невалидный токен
   - ✗ Access токен вместо refresh

---

## 🎯 Приоритеты задач

### Критично (сделать сейчас):
1. ✅ JWT функции (create, verify)
2. ✅ Pydantic схемы
3. ✅ Эндпоинт /register
4. ✅ Эндпоинт /login
5. ✅ get_current_user

### Важно (потом):
6. ✅ Refresh токен
7. ✅ Сброс пароля
8. ✅ Валидация сложности пароля

### Желательно:
9. Email подтверждение
10. OAuth 2.0 (Google, Facebook)
11. 2FA (TOTP)
12. Rate limiting

---

## 💡 Подсказки

**Как сгенерировать SECRET_KEY?**
```bash
openssl rand -hex 32
```

**Где хранить SECRET_KEY?**
```bash
# В .env файле
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
```

**Как использовать токен в запросе?**
```bash
curl -H "Authorization: Bearer <token>" http://api/endpoint
```

**Как получить текущего пользователя?**
```python
@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return {"username": user.username}
```

---

## ❓ Частые вопросы

**Q: Почему access токен короткий?**  
A: Для безопасности. Если украден, действует недолго. Refresh токен обновляет.

**Q: Как отозвать токен?**  
A: JWT токены нельзя отозвать. Решение: хранить refresh токены в БД или использовать blacklist.

**Q: Нужно ли хранить пароли?**  
A: НЕТ! Только хеш. Никогда не храните пароли в открытом виде.

**Q: Что делать при утечке SECRET_KEY?**  
A: Сменить SECRET_KEY. Все токены станут недействительными. Пользователи должны войти заново.

---

## 📚 Полезные ссылки

- [JWT.io](https://jwt.io/) - декодер JWT токенов
- [Python-Jose](https://python-jose.readthedocs.io/) - JWT для Python
- [Passlib](https://passlib.readthedocs.io/) - хеширование паролей
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## 🚀 Быстрый старт

**Порядок реализации:**
1. Создать SECRET_KEY в .env
2. Реализовать JWT функции в services.py
3. Создать schemas.py
4. Реализовать /register
5. Реализовать /login
6. Реализовать get_current_user
7. Тестировать через Swagger

**Время:** ~3-4 часа на базовый функционал
