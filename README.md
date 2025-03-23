# insight-api

🚀 **Insight API** — REST API на базе FastAPI для обслуживания предсказаний модели машинного обучения.

Проект демонстрирует:
- Аутентификацию с помощью Basic Auth
- Предсказания модели через REST API
- Чистую архитектуру Python-проекта с использованием `src/`-структуры
- Структурированное логирование через `structlog`
- Загрузку конфигурации из `.env` с помощью Pydantic Settings
- Middleware для трассировки и корреляции запросов

---

## 📦 Возможности

- ✅ REST API для инференса ML модели
- 🔐 Аутентификация по логину и паролю
- 🧠 Поддельная база данных пользователей (in-memory)
- 🧠 Заглушка модели для имитации предсказаний
- 📊 Логирование с `X-Request-ID` и контекстом запроса
- ⚙️ Настройки окружения через `.env.local` и переменные `APP_ENV`
- 📂 Современная структура проекта (`src/`, Poetry, Ruff, Mypy)

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/therealalexmois/insight-api
cd insight-api
```

### 2. Установить зависимости

```bash
make install
```

Для установки зависимостей разработчика:

```bash
make install-dev
```

### 3. Создать .env.local

```bash
cp .env.sample .env.local
```

При необходимости отредактируйте файл.

### 4. Запустить приложение

```bash
make start
```

Приложение будет доступно по адресу http://127.0.0.1:8000


## 🔐 Примеры запросов

### Получение текущего пользователя

```bash
curl -u john_doe:dev_secret http://localhost:8000/users/me
```

### Предсказание по данным

```bash
curl -X POST http://localhost:8000/predict/ \
  -u john_doe:dev_secret \
  -H 'Content-Type: application/json' \
  -d '{"age": 42}'
```

## 🧪 Тестирование

```bash
make test
```

Или с покрытием:

```bash
make test-with-coverage
```

## 🧹 Проверка качества кода

```bash
make lint        # Линтинг Ruff
make type-check  # Проверка типов Mypy
make pre-commit  # Все хуки pre-commit
```

## 🛠 Стек технологий
- FastAPI
- Pydantic v2
- Poetry
- Ruff
- Mypy
- Structlog

## 📄 Лицензия
MIT License © 2025 @therealalexmois
