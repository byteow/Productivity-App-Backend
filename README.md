# ⚙️ Productivity App — Backend

REST API backend для [AI-приложения продуктивности](https://github.com/byteow/Productivity-App). Построен на FastAPI с асинхронной работой, JWT-авторизацией, фоновыми задачами через Celery и AI-интеграцией через OpenAI.

---

## ✨ Возможности

- 🔐 JWT-авторизация (access + refresh токены)
- 🤖 AI-функциональность через OpenAI API
- 📧 Отправка email-уведомлений
- ⚙️ Фоновые задачи через Celery + Redis
- 🗄 Async PostgreSQL через SQLAlchemy + asyncpg
- 🌐 Настраиваемый CORS
- 🐳 Полный деплой через Docker Compose + Nginx

---

## 🛠 Стек технологий

| Слой | Технологии |
|---|---|
| Фреймворк | FastAPI, Python 3.11+ |
| База данных | PostgreSQL + asyncpg + SQLAlchemy (async) |
| Миграции | Alembic |
| Авторизация | JWT (access + refresh) |
| Очереди | Celery + Redis |
| AI | OpenAI API |
| Email | SMTP (aiosmtplib) |
| Прокси / деплой | Nginx, Docker, Docker Compose |

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/byteow/Productivity-App-Backend.git
cd Productivity-App-Backend
```

### 2. Настрой переменные окружения

```bash
cp .env.example .env
```

### 3. Запусти через Docker Compose

```bash
docker compose up -d --build
```

### 4. Примени миграции

```bash
docker compose exec app alembic upgrade head
```

API доступно на `http://localhost/api` ✅  
Документация Swagger: `http://localhost/docs`

---

## ⚙️ Переменные окружения

| Переменная | Описание |
|---|---|
| `PG_URI` | Строка подключения к PostgreSQL (`postgresql+asyncpg://...`) |
| `JWT_ACCESS_SECRET` | Секрет для access-токена |
| `JWT_REFRESH_SECRET` | Секрет для refresh-токена |
| `CELERY_BROKER_URL` | URL брокера Celery (`redis://...`) |
| `CELERY_RESULT_BACKEND` | URL бэкенда результатов Celery |
| `REDIS_URI` | URI подключения к Redis |
| `EMAIL_LOGIN` | Email-адрес для отправки писем |
| `EMAIL_PASSWORD` | Пароль от email |
| `EMAIL_SERVER` | SMTP-сервер (например `smtp.gmail.com`) |
| `EMAIL_SERVER_PORT` | Порт SMTP (обычно `587`) |
| `CORS_ORIGINS` | Разрешённые origins через запятую (обязательна запятая в конце) |
| `OPENAI_API_KEY` | Ключ OpenAI API |
| `OPENAI_PROXY` | Прокси для OpenAI (опционально) |

---

## 🐳 Запуск без Docker (локально)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# заполни .env

alembic upgrade head

# Запуск сервера
bash dev_app.sh

# Запуск Celery (в отдельном терминале)
bash dev_celery.sh
```

> Убедись, что PostgreSQL и Redis запущены локально.

---

## 📁 Структура проекта

```
Productivity-App-Backend/
├── src/                  # Основной код
│   ├── api/              # Роуты FastAPI
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   ├── services/         # Бизнес-логика, AI, email
│   ├── tasks/            # Celery задачи
│   └── core/             # Конфиг, безопасность
├── nginx/                # Конфиг Nginx
├── alembic/              # Миграции БД
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── dev_app.sh            # Скрипт запуска для разработки
└── dev_celery.sh         # Скрипт запуска Celery
```

---

## 🔗 Связанные репозитории

- [Productivity-App (Frontend)](https://github.com/byteow/Productivity-App) — React + TypeScript

---

## 👨‍💻 Автор

**byteow** — Full Stack Developer (Python / React)

- GitHub: [@byteow](https://github.com/byteow)
- Telegram: [@artembyteow](https://t.me/artembyteow)
