# 🚀 Быстрый запуск Ansar Store

## Запуск проекта

### 1. Запустить через Docker Compose
```bash
docker-compose up --build
```

### 2. Проверить что работает
Откройте в браузере:
- API: http://localhost:8000
- Документация: http://localhost:8000/docs

### 3. Применить миграции (если нужно)
```bash
docker-compose exec backend alembic upgrade head
```

## Тестовые запросы

### Создать тестового пользователя
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123456",
    "role": "user"
  }'
```

### Получить список товаров
```bash
curl "http://localhost:8000/api/v1/products/"
```

## Остановка
```bash
docker-compose down
```

## Очистка данных
```bash
docker-compose down -v
```

## Проблемы?

### База данных не подключается
Подождите 5-10 секунд после запуска - PostgreSQL нужно время для инициализации

### Ошибка импорта
```bash
docker-compose down
docker-compose up --build
```

### Порт занят
Измените порт в docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Вместо 8000:8000
```


