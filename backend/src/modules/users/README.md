# 👥 Модуль Users (Пользователи)

> **Часть проекта:** Ansar Store - Интернет-магазин  
> **Назначение:** Управление пользователями и их правами доступа

---

## 📌 Контекст проекта

Модуль Users - это основа всей системы аутентификации и авторизации. Определяет КТО работает с системой и ЧТО может делать. Тесно связан с Auth (вход/выход), Orders (заказы пользователя) и Notification (настройки уведомлений).

**Роль в системе:** Управление профилями, ролями и правами доступа для всех участников системы.

---

## ✅ Текущий статус: 70%

**Что работает:**
- ✅ Модель User с ролями (USER, ADMIN, MANAGER)
- ✅ CRUD операции (асинхронные)
- ✅ API эндпоинты для управления пользователями
- ✅ Связи с Cart и Orders

**Что требует реализации:**
- ⚠️ Хеширование паролей при создании через API
- ⚠️ Проверка JWT токенов (depends.py - заглушка)
- ⚠️ Проверка ролей для защищенных эндпоинтов
- ⚠️ Интеграция с Auth модулем

---

## 🎯 Цель модуля

**После полной реализации пользователи смогут:**
1. Регистрироваться с проверкой уникальности email/username
2. Управлять своим профилем (изменять данные, пароль)
3. Видеть историю своих заказов
4. Настраивать уведомления
5. Сохранять адреса доставки
6. Иметь избранные товары (wishlist)

**Администраторы смогут:**
1. Просматривать всех пользователей
2. Блокировать/разблокировать аккаунты
3. Изменять роли пользователей
4. Просматривать статистику по пользователям

**Менеджеры смогут:**
1. Просматривать пользователей
2. Помогать с заказами клиентов

---

## 📊 Структура модуля

```
users/
├── models.py     # User, UserRole
├── schemas.py    # Pydantic схемы валидации
├── crud.py       # Операции с БД (async)
├── routers.py    # API эндпоинты
├── services.py   # ⚠️ Бизнес-логика (минимально)
└── depends.py    # ⚠️ Проверка JWT и ролей (ЗАГЛУШКА)
```

---

## 🔗 API Эндпоинты

```
POST   /api/v1/users/              Создать пользователя
GET    /api/v1/users/              Получить всех пользователей
GET    /api/v1/users/{id}          Получить пользователя по ID
PATCH  /api/v1/users/{id}/status   Изменить статус (активен/заблокирован)
DELETE /api/v1/users/{id}          Удалить пользователя
```

---

## 📝 Техническое задание

### 1. Хеширование паролей (КРИТИЧНО!)
**Проблема:** Пароли сохраняются в открытом виде

**Где исправить:** `crud.py` → функция `create_user`

**Что нужно сделать:**
```python
from modules.auth.services import hash_password

async def create_user(...):
    # ДО: password=password
    # ПОСЛЕ:
    hashed_password = hash_password(password)
    
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,  # ← Хешированный!
        ...
    )
```

**Подсказка:** Функция `hash_password` уже реализована в `modules.auth.services`

---

### 2. Проверка JWT токенов (КРИТИЧНО!)
**Проблема:** `depends.py` - это заглушка, не проверяет токены

**Где реализовать:** `depends.py`

**Что нужно сделать:**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    1. Декодировать JWT токен (использовать jwt.decode)
    2. Извлечь user_id из payload
    3. Получить пользователя из БД
    4. Проверить is_active
    5. Вернуть User
    
    При ошибке - HTTPException 401
    """
```

**Подсказка:** 
- SECRET_KEY и ALGORITHM должны совпадать с Auth модулем
- Используйте `from modules.auth.services import verify_token`

---

### 3. Проверка ролей (КРИТИЧНО!)
**Проблема:** `role_deps` не работает, любой может получить доступ

**Где исправить:** `depends.py`

**Что нужно сделать:**
```python
def require_roles(*allowed_roles: str):
    """
    Декоратор для проверки роли пользователя
    
    Использование:
    @router.get("/", dependencies=[Depends(require_roles("admin", "manager"))])
    """
    async def check_role(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав"
            )
        return current_user
    
    return check_role
```

**Использование в routers.py:**
```python
# Было:
dependencies=[role_deps("admin", "manager")]

# Стало:
dependencies=[Depends(require_roles("admin", "manager"))]
```

---

### 4. Обновление routers.py (ВАЖНО!)
**Задача:** Использовать `current_user` вместо передачи user_id

**Что нужно исправить:**

```python
# БЫЛО (небезопасно):
@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(...)):
    user = await crud.get_user_by_id(db, user_id)

# СТАЛО (безопасно):
@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(...)
):
    return current_user
```

**Подсказка:** Для получения чужого профиля (admin) создать отдельный эндпоинт

---

### 5. Валидация данных (ВАЖНО!)
**Задача:** Усилить валидацию в schemas.py

**Что добавить:**
```python
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password_strength(cls, v):
        """
        Проверка сложности пароля:
        - Минимум 8 символов
        - Хотя бы одна цифра
        - Хотя бы одна заглавная буква
        """
        if not any(char.isdigit() for char in v):
            raise ValueError('Пароль должен содержать цифры')
        if not any(char.isupper() for char in v):
            raise ValueError('Пароль должен содержать заглавные буквы')
        return v
```

---

### 6. Смена пароля (СРЕДНИЙ ПРИОРИТЕТ)
**Задача:** Пользователь может изменить свой пароль

**Где реализовать:** `services.py`

**Что нужно:**
1. Создать схему `PasswordChange` в schemas.py
2. Создать функцию в services.py
3. Добавить эндпоинт в routers.py

**Схема:**
```python
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Пароли не совпадают')
        return v
```

**Логика в services.py:**
```python
async def change_password(
    db: AsyncSession,
    user: User,
    old_password: str,
    new_password: str
) -> bool:
    """
    1. Проверить старый пароль (verify_password)
    2. Захешировать новый пароль (hash_password)
    3. Обновить user.password
    4. Сохранить в БД
    """
```

---

### 7. История активности (НИЗКИЙ ПРИОРИТЕТ)
**Задача:** Логировать действия пользователя

**Что нужно:**
1. Создать модель `UserActivity` в models.py
2. Записывать важные события (вход, изменение профиля, заказы)
3. Эндпоинт для просмотра истории

**Структура UserActivity:**
- user_id: FK
- action_type: str (login, profile_update, order_created)
- description: str
- ip_address: str
- created_at: datetime

---

## 🔍 Важные детали

### UserRole (роли пользователей)
```python
class UserRole(Enum):
    USER = "user"         # Обычный покупатель
    MANAGER = "manager"   # Менеджер магазина
    ADMIN = "admin"       # Администратор системы
```

**Права доступа:**
- `USER`: свой профиль, свои заказы, каталог
- `MANAGER`: все заказы, все пользователи (только чтение), каталог
- `ADMIN`: полный доступ ко всему

### Связи модели User
```python
User.cart          → Cart (one-to-one)
User.orders        → List[Order] (one-to-many)
User.reviews       → List[Review] (one-to-many)
User.notifications → List[Notification] (one-to-many)
```

---

## 🧪 Тестовые сценарии

### Для реализации:

1. **Регистрация:**
   - ✓ Уникальный username и email
   - ✗ Дубликат username
   - ✗ Дубликат email
   - ✓ Пароль хешируется
   - ✗ Слабый пароль

2. **Аутентификация:**
   - ✓ Правильный логин/пароль → токен
   - ✗ Неправильный пароль
   - ✗ Несуществующий пользователь
   - ✗ Заблокированный пользователь

3. **Права доступа:**
   - ✓ USER видит только свой профиль
   - ✗ USER не может видеть чужие профили
   - ✓ ADMIN видит все профили
   - ✓ MANAGER видит все профили (read-only)

---

## 🎯 Приоритеты задач

### Критично (сделать сейчас):
1. ✅ Хеширование паролей при создании
2. ✅ Реализовать `get_current_user` в depends.py
3. ✅ Реализовать `require_roles` в depends.py
4. ✅ Обновить routers.py для использования current_user

### Важно (сделать потом):
5. ✅ Усилить валидацию паролей
6. ✅ Смена пароля
7. ✅ Обновление профиля
8. ✅ Проверка уникальности email/username при обновлении

### Желательно (можно добавить позже):
9. История активности
10. Аватары пользователей
11. Множественные адреса доставки
12. Настройки уведомлений

---

## 💡 Подсказки

**Как проверить JWT токен?**
```python
from jose import jwt, JWTError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = int(payload.get("sub"))
except JWTError:
    raise HTTPException(401, "Invalid token")
```

**Как проверить пароль?**
```python
from modules.auth.services import verify_password

if not verify_password(plain_password, user.password):
    raise HTTPException(401, "Неверный пароль")
```

**Как получить текущего пользователя в эндпоинте?**
```python
from modules.users.depends import get_current_user

@router.get("/me")
async def my_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

---

## ❓ Частые вопросы

**Q: Где хранить SECRET_KEY для JWT?**  
A: В файле `.env` (переменная окружения), НЕ в коде!

**Q: Как разделить права USER и ADMIN?**  
A: Используйте `Depends(require_roles("admin"))` в декораторе эндпоинта

**Q: Можно ли изменить свою роль?**  
A: Нет! Роль может изменить только ADMIN через отдельный эндпоинт

**Q: Что делать с удаленными пользователями?**  
A: Лучше не удалять физически, а ставить `is_active=False` (мягкое удаление)

---

## 📚 Полезные ссылки

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [JWT (PyJWT)](https://pyjwt.readthedocs.io/)
