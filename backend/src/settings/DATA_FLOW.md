# Потоки данных и хранение информации

Документ описывает, какие настройки задействованы в проекте и как данные
передаются между компонентами.

## 1. Переменные окружения (`.env`)

Все чувствительные параметры задаются в файле `.env` в корне проекта.
Минимальный набор:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/mydb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

Docker‑контейнер автоматически подхватывает эти значения, потому что
`settings.Settings` ищет `.env` в рабочей директории.

**Как сгенерировать `SECRET_KEY`:**

```bash
openssl rand -hex 32
# или
python - <<'PY'
import secrets
print(secrets.token_hex(32))
PY
```

Скопируйте полученную строку в `.env`:

```
SECRET_KEY=ваша_строка_из_32_символов
```

## 2. Настройки приложения (`settings/settings.py`)

Модуль `settings` — единая точка доступа к переменным окружения.

```python
from settings.settings import get_settings

settings = get_settings()
settings.database_url  # строка подключения к БД
```

Экземпляр кэшируется, поэтому настройки читаются только один раз.

## 3. Подключение к базе (`db/database.py`)

1. Берём URL из `settings.database_url`.
2. Создаём `create_async_engine(...)`.
3. Настраиваем `async_sessionmaker` (без автоматического expire).
4. Любая бизнес‑логика получает сессию через `Depends(get_async_session)`.

Это гарантирует единый пул соединений и корректное закрытие сессий.

## 4. Модели и миграции

- Все модели объявлены в `modules/*/models.py` и наследуются от `Base`.
- Alembic расположен в `backend/src/alembic/`.
- Конфигурация в `backend/alembic.ini`.
- Генерация миграции:
  ```bash
  docker compose exec backend alembic revision --autogenerate -m "message"
  docker compose exec backend alembic upgrade head
  ```

## 5. Где хранятся данные

- **База данных:** PostgreSQL (контейнер `db`), схема `public`.
- **Миграции:** `backend/src/alembic/versions/`.
- **Настройки:** `.env` + `settings/settings.py`.
- **Структура API:** собирается в `modules/__init__.py` и подключается в `main.py`.

## 6. Как проходит запрос

1. Клиент вызывает endpoint FastAPI.
2. Роутер получает сессию через `Depends(get_async_session)`.
3. Crud/сервисы работают с моделями и БД.
4. Результат преобразуется в Pydantic‑схемы и отправляется клиенту.

Это разделение упрощает тестирование и соблюдает единый стиль хранения данных.


