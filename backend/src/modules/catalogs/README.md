# 🛍️ Модуль Catalogs (Каталог товаров)

> **Часть проекта:** Ansar Store - Интернет-магазин  
> **Назначение:** Управление товарами, категориями, брендами и отзывами

---

## 📌 Контекст проекта

Модуль Catalogs - это витрина магазина. Здесь хранятся все товары с описаниями, ценами, изображениями. Связан с Orders (что заказывают), Users (кто оставляет отзывы), Notification (уведомления о товарах).

**Роль в системе:** Предоставить удобный способ поиска и выбора товаров для покупки.

---

## ✅ Текущий статус: 60%

**Что работает:**
- ✅ Модели Product, Category, Brand, Tag, Review, ProductImage
- ✅ Базовые CRUD операции
- ✅ API эндпоинты (список, создание, детали товара)

**Что требует реализации:**
- ⚠️ Поиск и фильтрация товаров
- ⚠️ Отзывы без связи с User
- ⚠️ Загрузка изображений
- ⚠️ Вложенные категории
- ⚠️ Расчет среднего рейтинга

---

## 🎯 Цель модуля

**После полной реализации покупатели смогут:**
1. Искать товары по названию и описанию
2. Фильтровать по категории, бренду, цене
3. Сортировать (популярность, цена, рейтинг)
4. Просматривать детали товара с фото
5. Читать отзывы других покупателей
6. Оставлять свои отзывы с рейтингом
7. Добавлять товары в избранное
8. Сравнивать товары
9. Подписываться на уведомления о поступлении

**Менеджеры смогут:**
1. Добавлять новые товары
2. Редактировать информацию о товарах
3. Управлять остатками на складе
4. Загружать изображения
5. Модерировать отзывы
6. Создавать акции и скидки

---

## 📊 Структура модуля

```
catalogs/
├── models.py     # Product, Category, Brand, Tag, Review, ProductImage
├── crud.py       # CRUD операции (частично)
├── services.py   # Бизнес-логика (минимально)
└── routers.py    # API эндпоинты (базовые)
```

---

## 🔗 API Эндпоинты

**Текущие:**
```
GET    /api/v1/products/           Список товаров
POST   /api/v1/products/           Создать товар
GET    /api/v1/products/{id}       Детали товара
```

**Требуется добавить:**
```
PUT    /api/v1/products/{id}       Обновить товар
DELETE /api/v1/products/{id}       Удалить товар
GET    /api/v1/products/search     Поиск товаров
GET    /api/v1/products/filter     Фильтрация

GET    /api/v1/categories/         Категории (дерево)
GET    /api/v1/brands/             Бренды

GET    /api/v1/products/{id}/reviews    Отзывы товара
POST   /api/v1/products/{id}/reviews    Создать отзыв
```

---

## 📝 Техническое задание

### 1. Поиск товаров (ВАЖНО!)
**Задача:** Реализовать полнотекстовый поиск

**Где реализовать:** `crud.py`

```python
async def search_products(
    session: AsyncSession,
    query: str,
    skip: int = 0,
    limit: int = 100
) -> list[Product]:
    """
    Поиск по:
    - Product.name (ILIKE)
    - Product.description (ILIKE)
    - Product.characteristic (ILIKE)
    
    Использовать OR условие для поиска по всем полям
    
    Подсказка:
    from sqlalchemy import or_
    
    stmt = select(Product).where(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%"),
            Product.characteristic.ilike(f"%{query}%")
        )
    )
    """
```

**Добавить эндпоинт:**
```python
@router.get("/search")
async def search_products(
    q: str,  # Query параметр для поиска
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    products = await crud.search_products(session, q, skip, limit)
    return products
```

---

### 2. Фильтрация товаров (ВАЖНО!)
**Задача:** Фильтры по категории, бренду, цене, наличию

**Где реализовать:** `crud.py`

```python
async def filter_products(
    session: AsyncSession,
    category_id: int | None = None,
    brand_id: int | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    in_stock: bool | None = None,
    skip: int = 0,
    limit: int = 100
) -> list[Product]:
    """
    1. Начать с select(Product)
    2. Добавлять WHERE условия, если параметр указан
    3. Пример:
       if category_id:
           stmt = stmt.where(Product.category_id == category_id)
    4. Добавить offset, limit
    5. Вернуть список
    """
```

---

### 3. Отзывы с пользователями (КРИТИЧНО!)
**Проблема:** Review не связана с User

**Где исправить:** `models.py`

```python
class Review(Base):
    __tablename__ = 'reviews'
    
    # Существующие поля...
    
    # ДОБАВИТЬ:
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    is_verified_purchase: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    helpful_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="reviews")
```

**CRUD для отзывов:**
```python
async def create_review(
    session: AsyncSession,
    product_id: int,
    user_id: int,
    rating: int,  # 1-5
    description: str
) -> Review:
    """
    1. Проверить, не оставлял ли user уже отзыв на этот товар
    2. Валидировать rating (1-5)
    3. Создать Review
    4. Пересчитать средний рейтинг товара
    """
```

---

### 4. Средний рейтинг товара (ВАЖНО!)
**Задача:** Рассчитывать средний рейтинг по отзывам

**Где реализовать:** `services.py`

```python
async def calculate_average_rating(
    session: AsyncSession,
    product_id: int
) -> float:
    """
    1. Получить все отзывы товара
    2. Суммировать rating
    3. Разделить на количество отзывов
    4. Округлить до 1 знака (round(x, 1))
    5. Вернуть число
    
    Можно использовать SQL агрегацию:
    from sqlalchemy import func
    
    result = await session.execute(
        select(func.avg(Review.rating))
        .where(Review.product_id == product_id)
    )
    """
```

**Добавить поле в Product:**
```python
class Product(Base):
    # ...
    average_rating: Mapped[float | None] = mapped_column(
        Float,
        default=0.0
    )
```

---

### 5. Загрузка изображений (СРЕДНИЙ ПРИОРИТЕТ)
**Задача:** Позволить загружать изображения товаров

**Что нужно:**

**Эндпоинт для загрузки:**
```python
from fastapi import UploadFile, File

@router.post("/{product_id}/images")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    is_main: bool = False,
    session: AsyncSession = Depends(get_async_session)
):
    """
    1. Проверить тип файла (image/jpeg, image/png)
    2. Проверить размер (макс 5MB)
    3. Сгенерировать уникальное имя файла
    4. Сохранить в /static/products/{product_id}/
    5. Создать запись ProductImage с URL
    6. Если is_main=True, сбросить флаг у других изображений
    """
```

**Подсказка:**
```python
import aiofiles
import uuid

# Путь для сохранения
filename = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
filepath = f"static/products/{product_id}/{filename}"

# Сохранение
async with aiofiles.open(filepath, 'wb') as f:
    content = await file.read()
    await f.write(content)

# URL для доступа
url = f"/static/products/{product_id}/{filename}"
```

---

### 6. Вложенные категории (СРЕДНИЙ ПРИОРИТЕТ)
**Задача:** Поддержка подкатегорий (дерево категорий)

**Где исправить:** `models.py`

```python
class Category(Base):
    __tablename__ = 'categories'
    
    # Существующие поля...
    
    # ДОБАВИТЬ:
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id'),
        nullable=True
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    # Самореференция для дерева
    parent: Mapped["Category"] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent"
    )
```

**Получение дерева категорий:**
```python
async def get_categories_tree(
    session: AsyncSession
) -> list[Category]:
    """
    Получить только корневые категории (parent_id = None)
    SQLAlchemy автоматически загрузит children
    """
    stmt = select(Category).where(Category.parent_id == None)
    result = await session.execute(stmt)
    return list(result.scalars().all())
```

---

### 7. Проверка наличия товара (ВАЖНО!)
**Задача:** Функция для проверки перед добавлением в корзину

**Где реализовать:** `services.py`

```python
async def check_product_availability(
    session: AsyncSession,
    product_id: int,
    quantity: int
) -> tuple[bool, str]:
    """
    Проверка наличия товара
    
    Возвращает:
    - (True, "") если товар доступен
    - (False, "причина") если недоступен
    
    Проверки:
    1. Товар существует
    2. product.in_stock == True
    3. product.availability_count >= quantity
    
    Примеры:
    - (False, "Товар не найден")
    - (False, "Товара нет в наличии")
    - (False, "Доступно только X шт")
    - (True, "")
    """
```

---

### 8. Связанные товары (НИЗКИЙ ПРИОРИТЕТ)
**Задача:** Показывать похожие товары

**Где реализовать:** `services.py`

```python
async def get_related_products(
    session: AsyncSession,
    product_id: int,
    limit: int = 10
) -> list[Product]:
    """
    Найти похожие товары по:
    - Той же категории
    - Тому же бренду
    - Похожим тегам
    
    Исключить сам товар из результатов
    """
```

---

## 🔍 Важные детали

### Структура Product
```python
Product:
  - Основное: id, name, description, characteristic
  - Цена: price, discount_price (опционально)
  - Наличие: in_stock, availability_count
  - Мета: created_at, updated_at, average_rating
  - Связи: category, brand, images, tags, reviews
```

### Связи между моделями
```
Product → Category (many-to-one)
Product → Brand (many-to-one)
Product ← → Tag (many-to-many через product_tags)
Product → ProductImage (one-to-many)
Product → Review (one-to-many)
Review → User (many-to-one)
```

### Валидация рейтинга
```python
# В схеме ReviewCreate
rating: int = Field(..., ge=1, le=5)  # От 1 до 5
```

---

## 🧪 Тестовые сценарии

1. **Поиск:**
   - ✓ Поиск по названию
   - ✓ Поиск по описанию
   - ✓ Пустой запрос → все товары

2. **Фильтрация:**
   - ✓ По категории
   - ✓ По бренду
   - ✓ По цене (мин-макс)
   - ✓ Только в наличии
   - ✓ Комбинация фильтров

3. **Отзывы:**
   - ✓ Создание отзыва
   - ✗ Дубликат отзыва от того же пользователя
   - ✓ Обновление среднего рейтинга
   - ✗ Рейтинг вне диапазона 1-5

---

## 🎯 Приоритеты задач

### Критично:
1. ✅ Поиск товаров
2. ✅ Фильтрация товаров
3. ✅ Связь Review с User
4. ✅ Расчет среднего рейтинга

### Важно:
5. ✅ CRUD для отзывов
6. ✅ Проверка наличия товара
7. ✅ Загрузка изображений

### Желательно:
8. Вложенные категории
9. Связанные товары
10. Избранное (wishlist)
11. Сравнение товаров

---

## 💡 Подсказки

**Как сделать поиск без учета регистра?**
```python
Product.name.ilike(f"%{query}%")  # ILIKE = case-insensitive
```

**Как комбинировать фильтры?**
```python
stmt = select(Product)
if category_id:
    stmt = stmt.where(Product.category_id == category_id)
if min_price:
    stmt = stmt.where(Product.price >= min_price)
# и так далее
```

**Как загрузить связанные данные?**
```python
from sqlalchemy.orm import selectinload

stmt = select(Product).options(
    selectinload(Product.images),
    selectinload(Product.category),
    selectinload(Product.brand)
)
```

---

## ❓ Частые вопросы

**Q: Где хранить изображения?**  
A: В папке `static/products/{product_id}/` или использовать CDN/S3

**Q: Как ограничить количество отзывов от одного пользователя?**  
A: Добавить unique constraint на (product_id, user_id)

**Q: Нужно ли модерировать отзывы?**  
A: Да, лучше добавить поле `is_approved` и проверку админом

**Q: Как сделать slug для SEO?**  
A: Добавить поле `slug` в Product и генерировать из name (python-slugify)

---

## 📚 Полезные ссылки

- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationship_api.html)
- [FastAPI File Upload](https://fastapi.tiangolo.com/tutorial/request-files/)
- [Pillow](https://pillow.readthedocs.io/) - обработка изображений
