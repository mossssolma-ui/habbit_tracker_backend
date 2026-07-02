# Habit Tracker Backend

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-red.svg)](https://www.django-rest-framework.org/)
[![Coverage](https://img.shields.io/badge/Coverage-83%25-brightgreen.svg)]()

Backend-часть SPA-приложения для трекера полезных привычек, реализованная на Django REST Framework.

## О проекте

Проект представляет собой бэкенд для сервиса трекера полезных привычек, вдохновленного книгой Джеймса Клира «Атомные
привычки». Приложение позволяет пользователям создавать, редактировать и отслеживать свои привычки, а также получать
напоминания через Telegram-бота.

### Основные возможности

- Регистрация и авторизация пользователей с JWT-токенами
- CRUD-операции с привычками
- Пагинация (5 привычек на страницу)
- Фильтрация привычек по публичности и месту
- Интеграция с Telegram для отправки напоминаний
- Отложенные задачи через Celery + Redis
- Полная документация API (Swagger/ReDoc)
- Покрытие тестами ~83%
- Настроен CORS для взаимодействия с фронтендом

## Технологии

- Python 3.14
- Django 6.0
- Django REST Framework 3.17
- PostgreSQL
- Redis (брокер для Celery)
- Celery (отложенные задачи)
- Django Celery Beat (планировщик)
- JWT-аутентификация
- drf-yasg (Swagger/ReDoc документация)
- Poetry (управление зависимостями)
- Docker + Docker Compose
- Coverage (тестовое покрытие)

## Установка и запуск

### Требования

- Python 3.14+
- Poetry
- PostgreSQL
- Redis
- Celery

### Локальная установка

1. **Клонируйте репозиторий:**

```bash
git clone git@github.com:mossssolma-ui/habbit_tracker_backend.git
```

2. **Установите зависимости через Poetry:**

```bash
poetry install
```

3. **Создайте файл .env и заполните его:**

```Пример заполнения
SECRET_KEY=django-insecure-9x4f7k2p8w5sdfsdfq9r2t8y............

DEBUG=True

DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=habit_tracker_backend
DB_USER=postgres
DB_PASSWORD=Z1xcv.......
DB_HOST=localhost
DB_PORT=5432

CSU_EMAIL=admin@mail.ru
CSU_PASSWORD=Z1xcv......

TG_API_KEY=123143........
TELEGRAM_URL=https://api.telegram.org/bot

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=0
```

4. **Примените миграции:**

```bash
python manage.py migrate
```

5. **Создайте суперпользователя (из переменных .env):**

```bash
python manage.py csu
```

6. **Запустите Redis (для Celery):**

```bash
redis-server
```

7. **Запустите Celery worker (в отдельном терминале):**

```bash
celery -A config worker -l info -P eventlet
```

8. **Запустите Celery beat (в отдельном терминале):**

```bash
celery -A config beat -l info
```

9. **Запустите сервер:**

```bash
python manage.py runserver
```

## Модель данных

### Привычка (Habit)

| Поле                | Тип                  | Описание                    |
|---------------------|----------------------|-----------------------------|
| `user`              | ForeignKey           | Создатель привычки          |
| `place`             | CharField            | Место выполнения            |
| `time`              | TimeField            | Время выполнения            |
| `action`            | CharField            | Действие привычки           |
| `is_pleasant_habit` | BooleanField         | Признак приятной привычки   |
| `related_habit`     | ForeignKey           | Связанная привычка          |
| `frequency`         | PositiveIntegerField | Периодичность (1-7 дней)    |
| `reward`            | CharField            | Вознаграждение              |
| `time_to_complete`  | PositiveIntegerField | Время выполнения (≤120 сек) |
| `is_public`         | BooleanField         | Публичность                 |
| `created_at`        | DateTimeField        | Дата создания               |
| `updated_at`        | DateTimeField        | Дата обновления             |

### Пользователь

| Поле           | Тип        | Описание                      |
|----------------|------------|-------------------------------|
| `email`        | EmailField | Логин (уникальный)            |
| `first_name`   | CharField  | Имя                           |
| `last_name`    | CharField  | Фамилия                       |
| `phone_number` | CharField  | Телефон                       |
| `city`         | CharField  | Город                         |
| `avatar`       | ImageField | Аватар                        |
| `tg_chat_id`   | CharField  | ID в Telegram для уведомлений |

## Валидация

При создании привычек реализованы следующие проверки:

* Нельзя одновременно указать reward и related_habit
* time_to_complete не может превышать 120 секунд
* related_habit может быть только приятной привычкой
* У приятной привычки не может быть reward или related_habit
* frequency должна быть в диапазоне 1-7 дней

## Права доступа

IsAuthenticated - для списка и создания привычек
IsOwner - для просмотра, редактирования и удаления (только владелец)
AllowAny - для просмотра публичных привычек

## API Эндпоинты

### Пользователи

| Метод     | Эндпоинт                | Описание                | Права           |
|-----------|-------------------------|-------------------------|-----------------|
| POST      | `/users/register/`      | Регистрация             | AllowAny        |
| POST      | `/users/login/`         | Получение JWT токена    | AllowAny        |
| POST      | `/users/token/refresh/` | Обновление токена       | AllowAny        |
| GET       | `/users/`               | Список пользователей    | Superuser       |
| GET       | `/users/{id}/`          | Получение пользователя  | Owner/Superuser |
| PUT/PATCH | `/users/{id}/`          | Обновление пользователя | Owner/Superuser |
| DELETE    | `/users/{id}/`          | Удаление пользователя   | Superuser       |

### Привычки

| Метод     | Эндпоинт          | Описание                       | Права           |
|-----------|-------------------|--------------------------------|-----------------|
| GET       | `/habits/`        | Список привычек со статистикой | IsAuthenticated |
| POST      | `/habits/`        | Создание привычки              | IsAuthenticated |
| GET       | `/habits/{id}/`   | Просмотр привычки              | IsOwner         |
| PUT/PATCH | `/habits/{id}/`   | Обновление привычки            | IsOwner         |
| DELETE    | `/habits/{id}/`   | Удаление привычки              | IsOwner         |
| GET       | `/habits/public/` | Публичные привычки             | AllowAny        |

## Документация API

После запуска сервера документация доступна по адресам:

* Swagger UI: http://127.0.0.1:8000/swagger/
* ReDoc: http://127.0.0.1:8000/redoc/

## Telegram-бот

Проект интегрирован с Telegram для отправки напоминаний:

1. Создайте бота в Telegram через [@BotFather](https://t.me/BotFather)
2. Получите токен и добавьте в `.env` (`TG_API_KEY`)
3. Получите свой Telegram ID через [@userinfobot](https://t.me/userinfobot)
4. Укажите `tg_chat_id` для пользователя в админке
5. Уведомления отправляются автоматически в указанное время

## Тестирование

### Запуск тестов

```
python manage.py test
```

### Покрытие кода

```
 coverage report
```

## Структура проекта

```
habit_tracker_backend/
├── config/                 # Настройки проекта
│   ├── __init__.py
│   ├── asgi.py           
│   ├── wsgi.py           
│   ├── celery.py           
│   ├── settings.py         
│   └── urls.py             
├── htmlcov/                # Покрытие тестами
│   ├── index.html          
├── media/                  # Для хранения media
├── static/                 # Для хранения статики
│               
├── habits/                 # Приложение привычек
│   ├── admin.py            
│   ├── apps.py            
│   ├── models.py           
│   ├── views.py            
│   ├── serializers.py      
│   ├── exceptions.py      
│   ├── urls.py             
│   ├── validators.py           
│   ├── paginators.py       
│   ├── services.py         
│   ├── tasks.py            
│   └── tests.py            
│              
├── users/                  # Приложение пользователей
│   ├── management/
│   │   └── commands
│   │       └── csu.py      # Создание суперюзера
│   │  
│   ├── admin.py            
│   ├── apps.py            
│   ├── models.py 
│   ├── permissions.py            
│   ├── views.py            
│   ├── serializers.py      
│   ├── urls.py             
│   └── tests.py            
│ 
├── .env.template           # Шаблон переменных окружения
├── pyproject.toml          # Зависимости
└── README.md
```

## Лицензия

MIT License