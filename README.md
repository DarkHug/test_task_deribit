# Crypto Price Service

Сервис для периодического сбора цен криптовалют с биржи Deribit и предоставления REST API для работы с сохранёнными данными.

## Что делает

- Каждую минуту забирает актуальную цену `BTC_USD` и `ETH_USD` с Deribit через index price API
- Сохраняет тикер, цену и UNIX timestamp в PostgreSQL
- Предоставляет REST API на FastAPI для получения сохранённых данных

## Стек

- **Python 3.13**
- **FastAPI** + **uvicorn**
- **SQLAlchemy** (async) + **asyncpg**
- **aiohttp** — HTTP-клиент для Deribit
- **Celery + Redis** — периодические задачи
- **PostgreSQL 16**
- **uv** — менеджер зависимостей
- **Docker / Docker Compose**

---

## Быстрый старт

### Требования

- Docker
- Docker Compose

### 1. Клонировать репозиторий

```bash
git clone https://github.com/DarkHug/test_task_deribit.git
cd test_task_deribit
```

### 2. Создать `.env` файл

Содержимое `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/crypto_db
REDIS_URL=redis://redis:6379/0
DERIBIT_API_URL=https://test.deribit.com/api/v2
```

### 3. Запустить

```bash
docker compose up --build
```

Поднимутся три контейнера: `app`, `postgres`, `redis`.

Внутри контейнера `app` через `entrypoint.sh` запускаются три процесса: FastAPI, Celery worker и Celery beat.

API доступно по адресу: [http://localhost:8000](http://localhost:8000)

Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API

Все эндпоинты находятся под префиксом `/prices`. Параметр `ticker` обязателен у каждого метода

### `GET /prices/`

Возвращает все сохранённые записи по указанной валюте.

```
GET /prices/?ticker=BTC_USD
```

### `GET /prices/latest`

Возвращает последнюю сохранённую цену.

```
GET /prices/latest?ticker=ETH_USD
```

### `GET /prices/by-date`

Возвращает запись с точным совпадением по UNIX timestamp.

```
GET /prices/by-date?ticker=BTC_USD&timestamp=1710500000
```

### `GET /prices/test-deribit`

Тестовый эндпоинт, делает live-запрос к Deribit и возвращает текущие цены без сохранения в БД.

---

## Структура проекта

```
app/
├── api/
│   └── routes.py            # FastAPI роутер
├── clients/
│   └── deribit_client.py    # Async HTTP-клиент для Deribit
├── db/
│   ├── base.py              # DeclarativeBase
│   └── session.py           # Async engine и get_db dependency
├── models/
│   └── price.py             # SQLAlchemy модель Price
├── repositories/
│   └── price_repo.py        # Запросы к БД
├── schemas/
│   └── price_schema.py      # Pydantic схемы
├── services/
│   └── price_service.py     # Бизнес-логика
├── tasks/
│   ├── celery_app.py        # Инициализация Celery и beat schedule
│   └── price_tasks.py       # Celery-таск fetch_prices
├── config.py                # Настройки через pydantic-settings
└── main.py                  # Точка входа FastAPI
docker/
├── Dockerfile
└── entrypoint.sh
tests/
docker-compose.yml
pyproject.toml
```

---

## Design Decisions

### Асинхронный стек

FastAPI работает на asyncio, поэтому весь стек сделан async. Для PostgreSQL используется `asyncpg` через `SQLAlchemy AsyncSession`, для запросов к Deribit — `aiohttp`. Это позволяет не блокировать event loop на IO-операциях и нормально держать нагрузку.

### Celery + asyncio.run()

Celery не поддерживает async-таски нативно. Вся async-логика завёрнута во внутреннюю корутину `run()` внутри таска и запускается через `asyncio.run()`. С точки зрения Celery ничего не меняется — он вызвал функцию, она отработала и вернула результат. Без этого Python просто создал бы корутину и не выполнил её, выбросив `coroutine was never awaited`.

### Слоистая архитектура router -> service -> repository

Роутер не знает про SQL, репозиторий не знает про бизнес-правила. Такое разделение упрощает тестирование каждого слоя отдельно и позволяет менять детали реализации без правок во всём проекте.

### pydantic-settings для конфигурации

Все переменные окружения читаются через `pydantic-settings` с явной типизацией. Если переменная не задана, приложение не запустится с понятной ошибкой, а не упадёт где-то в рантайме.

### Создание таблиц при старте

`Base.metadata.create_all` вызывается в `startup`-событии FastAPI. Для этого проекта это удобно: не нужна отдельная команда для инициализации БД. В продакшене стоит заменить на Alembic-миграции.

### uv как менеджер зависимостей

`uv` заметно быстрее `pip` при установке зависимостей, что ощутимо при пересборке Docker-образа в процессе разработки.

### Один контейнер для app, worker и beat

FastAPI, Celery worker и Celery beat запускаются в одном контейнере через `entrypoint.sh`. Для проекта такого масштаба это оправдано. В реальном сервисе их стоит разнести по отдельным контейнерам для независимого масштабирования и перезапуска.
