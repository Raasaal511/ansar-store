# 🔔 Модуль Notification (Уведомления)

> **Часть проекта:** Ansar Store - Интернет-магазин  
> **Назначение:** Система уведомлений для информирования пользователей

---

## 📌 Контекст проекта

Модуль Notification - это коммуникационный центр системы. Информирует пользователей о важных событиях: заказы, товары, акции. Интегрируется со всеми модулями: Orders (статусы заказов), Catalogs (товары в наличии), Users (персональные уведомления).

**Роль в системе:** Держать пользователей в курсе всех важных событий через разные каналы связи.

---

## ✅ Текущий статус: 20%

**Что есть:**
- ✅ Базовая модель Notification
- ✅ Заглушка роутера

**Что требует реализации:**
- ⚠️ CRUD операции (полностью)
- ⚠️ NotificationService для отправки
- ⚠️ Типы уведомлений (enum)
- ⚠️ Связь с User
- ⚠️ Email интеграция
- ⚠️ WebSocket для real-time

---

## 🎯 Цель модуля

**После полной реализации пользователи смогут:**
1. Получать уведомления о статусе заказа
2. Узнавать о поступлении товара на склад
3. Быть в курсе акций и скидок
4. Получать уведомления на email
5. Настраивать, какие уведомления получать
6. Видеть историю уведомлений
7. Отмечать уведомления как прочитанные

**Система сможет:**
1. Автоматически уведомлять о важных событиях
2. Отправлять email рассылки
3. Отправлять SMS (опционально)
4. Push уведомления в браузер/мобильное приложение
5. Real-time уведомления через WebSocket
6. Telegram бот уведомления

---

## 📊 Структура модуля

```
notification/
├── models.py     # Notification, NotificationType
├── crud.py       # ⚠️ Операции с БД (ПУСТО!)
├── routers.py    # ⚠️ API эндпоинты (ЗАГЛУШКА!)
└── services.py   # ⚠️ NotificationService (ПУСТО!)
```

---

## 📝 Техническое задание

### 1. Расширить модель (КРИТИЧНО!)
**Проблема:** В модели нет связи с User и типа уведомления

**Где исправить:** `models.py`

**Что добавить:**
```python
from enum import Enum
from sqlalchemy import ForeignKey, Enum as SqlEnum

class NotificationType(str, Enum):
    """Типы уведомлений"""
    ORDER_CREATED = "order_created"           # Заказ создан
    ORDER_STATUS_CHANGED = "order_status_changed"  # Статус изменен
    PRODUCT_AVAILABLE = "product_available"   # Товар в наличии
    PRICE_DROP = "price_drop"                 # Цена снизилась
    SYSTEM = "system"                         # Системное

class Notification(Base):
    # Существующие поля...
    
    # ДОБАВИТЬ:
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), 
        nullable=False
    )
    notification_type: Mapped[NotificationType] = mapped_column(
        SqlEnum(NotificationType),
        nullable=False
    )
    related_entity_id: Mapped[int | None] = mapped_column(
        nullable=True
    )  # ID заказа/товара для ссылки
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="notifications")
```

**Подсказка:** Нужно создать миграцию после изменения модели!

---

### 2. CRUD операции (КРИТИЧНО!)
**Задача:** Реализовать базовые операции с уведомлениями

**Где реализовать:** `crud.py`

**Что нужно:**

**create_notification** - создание уведомления
```python
async def create_notification(
    db: AsyncSession,
    user_id: int,
    title: str,
    message: str,
    notification_type: NotificationType,
    related_entity_id: int | None = None
) -> Notification:
    """
    1. Создать объект Notification
    2. Добавить в БД (db.add)
    3. Сохранить (db.commit)
    4. Обновить (db.refresh)
    5. Вернуть объект
    """
```

**get_user_notifications** - получить уведомления пользователя
```python
async def get_user_notifications(
    db: AsyncSession,
    user_id: int,
    unread_only: bool = False,
    limit: int = 50
) -> list[Notification]:
    """
    1. SELECT * FROM notifications WHERE user_id = ?
    2. Если unread_only: добавить WHERE is_read = False
    3. ORDER BY created_at DESC
    4. LIMIT
    """
```

**mark_as_read** - отметить как прочитанное
```python
async def mark_as_read(
    db: AsyncSession,
    notification_id: int,
    user_id: int
) -> bool:
    """
    1. Найти уведомление по ID и user_id
    2. Установить is_read = True
    3. Сохранить
    4. Вернуть True/False (успех/провал)
    """
```

**get_unread_count** - количество непрочитанных
```python
async def get_unread_count(
    db: AsyncSession,
    user_id: int
) -> int:
    """
    SELECT COUNT(*) FROM notifications 
    WHERE user_id = ? AND is_read = False
    """
```

---

### 3. NotificationService (КРИТИЧНО!)
**Задача:** Централизованная отправка уведомлений

**Где реализовать:** `services.py`

**Базовая структура:**
```python
class NotificationService:
    """Сервис для отправки уведомлений"""
    
    @staticmethod
    async def notify_order_created(
        db: AsyncSession,
        user_id: int,
        order_id: int
    ):
        """
        Уведомление о создании заказа
        
        1. Сформировать текст: "Ваш заказ #{order_id} создан"
        2. Вызвать crud.create_notification
        3. Опционально: отправить email
        """
        await create_notification(
            db=db,
            user_id=user_id,
            title="Заказ создан",
            message=f"Ваш заказ #{order_id} успешно создан",
            notification_type=NotificationType.ORDER_CREATED,
            related_entity_id=order_id
        )
    
    @staticmethod
    async def notify_order_status_changed(
        db: AsyncSession,
        user_id: int,
        order_id: int,
        new_status: str
    ):
        """Уведомление об изменении статуса заказа"""
        pass  # Реализовать аналогично
    
    @staticmethod
    async def notify_product_available(
        db: AsyncSession,
        user_id: int,
        product_id: int,
        product_name: str
    ):
        """Уведомление о появлении товара"""
        pass  # Реализовать
```

**Подсказка:** Эти функции будут вызываться из других модулей (Orders, Catalogs)

---

### 4. API Эндпоинты (ВАЖНО!)
**Задача:** Создать полноценные роутеры

**Где реализовать:** `routers.py`

**Нужные эндпоинты:**

```python
@router.get("/")
async def get_notifications(
    unread_only: bool = False,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить уведомления текущего пользователя"""
    # Вызвать crud.get_user_notifications

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Количество непрочитанных"""
    # Вызвать crud.get_unread_count

@router.patch("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Отметить как прочитанное"""
    # Вызвать crud.mark_as_read

@router.patch("/read-all")
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """Отметить все как прочитанные"""
    # Цикл по всем непрочитанным
```

---

### 5. Pydantic схемы (ВАЖНО!)
**Задача:** Создать схемы валидации

**Где реализовать:** Создать `schemas.py`

```python
from pydantic import BaseModel
from datetime import datetime

class NotificationRead(BaseModel):
    """Схема для чтения уведомления"""
    id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    related_entity_id: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True
```

---

### 6. Email уведомления (СРЕДНИЙ ПРИОРИТЕТ)
**Задача:** Отправка уведомлений на email

**Где реализовать:** `services.py`

**Что нужно:**
```python
import aiosmtplib
from email.mime.text import MIMEText

async def send_email_notification(
    to_email: str,
    subject: str,
    body: str
):
    """
    1. Получить SMTP настройки из .env
    2. Создать MIMEText сообщение
    3. Отправить через aiosmtplib.send
    
    Настройки:
    - SMTP_HOST (smtp.gmail.com)
    - SMTP_PORT (587)
    - SMTP_USER
    - SMTP_PASSWORD
    """
```

**Добавить в NotificationService:**
```python
@staticmethod
async def notify_order_created(...):
    # Создать уведомление в БД
    await create_notification(...)
    
    # Отправить email
    await send_email_notification(
        to_email=user.email,
        subject="Заказ создан",
        body=f"Ваш заказ #{order_id} успешно создан!"
    )
```

---

### 7. WebSocket для real-time (НИЗКИЙ ПРИОРИТЕТ)
**Задача:** Мгновенные уведомления без перезагрузки

**Где реализовать:** `routers.py`

**Концепция:**
```python
from fastapi import WebSocket

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,  # JWT токен для аутентификации
    db: AsyncSession = Depends(get_async_session)
):
    """
    1. Проверить токен, получить user_id
    2. Подключить WebSocket
    3. В цикле проверять новые уведомления каждые N секунд
    4. Отправлять через websocket.send_json()
    """
```

**Использование на клиенте:**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/notifications/ws?token=...');
ws.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    // Показать уведомление
};
```

---

## 🔍 Важные детали

### Типы уведомлений и их использование
```
ORDER_CREATED          → При создании заказа (Orders модуль)
ORDER_STATUS_CHANGED   → При изменении статуса (Orders модуль)
PRODUCT_AVAILABLE      → Товар снова в наличии (Catalogs модуль)
PRICE_DROP             → Цена снизилась (Catalogs модуль)
SYSTEM                 → Системные уведомления (Admin)
```

### Связи с другими модулями
```
Notification ← Orders    (уведомления о заказах)
Notification ← Catalogs  (уведомления о товарах)
Notification → Users     (кому отправлять)
```

### Каналы доставки (приоритеты)
1. **In-app** (в приложении) - всегда
2. **Email** - важные события
3. **SMS** - критичные (опционально)
4. **Push** - для мобильных (опционально)
5. **Telegram** - по желанию пользователя (опционально)

---

## 🧪 Тестовые сценарии

### Базовые:
1. ✓ Создание уведомления
2. ✓ Получение списка уведомлений
3. ✓ Отметка как прочитанное
4. ✓ Подсчет непрочитанных
5. ✗ Пользователь видит только свои уведомления

### Интеграционные:
1. ✓ При создании заказа → уведомление
2. ✓ При изменении статуса → уведомление
3. ✓ Email отправляется корректно
4. ✓ WebSocket получает уведомления

---

## 🎯 Приоритеты задач

### Критично (основной функционал):
1. ✅ Расширить модель (user_id, type, related_entity_id)
2. ✅ Реализовать CRUD операции
3. ✅ Создать NotificationService
4. ✅ Реализовать API эндпоинты
5. ✅ Создать Pydantic схемы

### Важно (коммуникация):
6. ✅ Интеграция с Orders модулем
7. ✅ Интеграция с Catalogs модулем
8. ✅ Email уведомления

### Желательно (расширенное):
9. WebSocket для real-time
10. SMS уведомления (Twilio)
11. Push уведомления (Firebase)
12. Telegram бот
13. Настройки уведомлений пользователя

---

## 💡 Подсказки

**Как вызвать уведомление из Orders модуля?**
```python
# В orders/crud.py после создания заказа:
from modules.notification.services import NotificationService

await NotificationService.notify_order_created(
    db=db,
    user_id=user_id,
    order_id=order.id
)
```

**Как отправить email?**
```python
# Добавить в requirements.txt:
# aiosmtplib==2.0.2

import aiosmtplib
from email.mime.text import MIMEText

message = MIMEText("Текст письма")
message["From"] = "noreply@ansar-store.com"
message["To"] = user_email
message["Subject"] = "Заказ создан"

await aiosmtplib.send(
    message,
    hostname="smtp.gmail.com",
    port=587,
    username=SMTP_USER,
    password=SMTP_PASSWORD,
    use_tls=True
)
```

**Как создать миграцию после изменения модели?**
```bash
alembic revision --autogenerate -m "Add user_id and type to notifications"
alembic upgrade head
```

---

## ❓ Частые вопросы

**Q: Где хранить SMTP пароль?**  
A: В файле `.env`, НИКОГДА в коде!

**Q: Как не спамить пользователя уведомлениями?**  
A: Добавить настройки уведомлений для каждого пользователя (таблица UserNotificationSettings)

**Q: Нужно ли хранить все уведомления вечно?**  
A: Нет, лучше автоматически удалять старые (> 90 дней) через cron задачу

**Q: Как отправлять уведомления асинхронно?**  
A: Использовать Celery + Redis для фоновых задач (для продакшена)

---

## 📚 Полезные ссылки

- [aiosmtplib](https://aiosmtplib.readthedocs.io/) - асинхронный SMTP
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [Celery](https://docs.celeryq.dev/) - фоновые задачи

---

## 🚀 Быстрый старт реализации

**Шаг 1:** Расширить модель + миграция  
**Шаг 2:** Реализовать CRUD (5 функций)  
**Шаг 3:** Создать NotificationService (3 метода)  
**Шаг 4:** API эндпоинты (4 эндпоинта)  
**Шаг 5:** Интеграция с Orders  
**Шаг 6:** Email (опционально)

**Время:** ~4-6 часов на базовый функционал
