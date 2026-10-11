# Todo List API

Backend для личного списка задач на FastAPI и PostgreSQL. Пользователь создаёт аккаунт, получает JWT-токен при входе и работает со своими задачами.

## Возможности

- Регистрация и вход по имени пользователя и паролю.
- Хранение хешей паролей через pwdlib.
- Проверка JWT и получение текущего пользователя.
- Создание задач со статусом `active`.
- Получение списка задач и фильтрация по статусу.
- Получение отдельной задачи и отметка о её выполнении.
- Ограничение доступа к задачам по владельцу.

Поддерживаемые статусы: `active` и `completed`.

## Стек

Python 3.12, FastAPI, Pydantic, PostgreSQL, Psycopg 3, pwdlib, PyJWT и pydantic-settings.

Версии установленных библиотек сохранены в `requirements.txt`.

## Основные файлы

| Путь | Назначение |
| --- | --- |
| `backend/api.py` | Маршруты API, модели данных и получение текущего пользователя |
| `backend/db.py` | Подключение к PostgreSQL, SQL-запросы и проверка паролей |
| `backend/auth.py` | Создание и проверка JWT |
| `backend/config.py` | Загрузка и проверка настроек |
| `schema.sql` | Структура таблиц, автоматические ID и ограничения |
| `.env.example` | Образец переменных окружения |
| `requirements.txt` | Список библиотек и их версий |

## Локальный запуск

Инструкция рассчитана на Ubuntu 24.04 с установленными Python 3.12, Git, OpenSSL и запущенным сервером PostgreSQL. Дамп `schema.sql` создан PostgreSQL 16.15; для восстановления используйте сервер и клиент psql той же версии или более новой совместимой версии.

Настройка БД ниже предназначена для первого запуска с новой пустой базой.

### 1. Скачать проект и установить библиотеки

```bash
git clone https://github.com/KnyazevNick/todo-list.git
cd todo-list
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Остальные команды выполняются из корня проекта.

### 2. Создать роль и базу данных

Откройте psql от имени администратора PostgreSQL:

```bash
sudo -u postgres psql -X
```

Внутри psql выполните:

```sql
CREATE ROLE todo_app LOGIN;
\password todo_app
CREATE DATABASE todo_db;
\q
```

Команда `\password` запросит новый пароль роли. Этот пароль потребуется для `TODO_DB_PASSWORD`.

`todo_app` — роль PostgreSQL, через которую приложение подключается к БД. Аккаунты пользователей самого приложения создаются через `/register` и хранятся в таблице `users`.

### 3. Восстановить структуру и выдать права

```bash
sudo -u postgres psql -X -v ON_ERROR_STOP=1 -d todo_db < schema.sql
```

Эта команда выполняет SQL из файла в новой базе. `ON_ERROR_STOP=1` останавливает выполнение при первой ошибке.

Затем откройте psql для этой базы:

```bash
sudo -u postgres psql -X -d todo_db
```

Выдайте приложению права:

```sql
GRANT CONNECT ON DATABASE todo_db TO todo_app;
GRANT USAGE ON SCHEMA public TO todo_app;
GRANT SELECT, INSERT ON public.users TO todo_app;
GRANT SELECT, INSERT, UPDATE ON public.tasks TO todo_app;
\q
```

После восстановления таблицы пустые. `schema.sql` содержит определения объектов БД; аккаунты и задачи создаются через API.

### 4. Заполнить настройки

Создайте локальный файл настроек из образца:

```bash
cp -n .env.example .env
```

Флаг `-n` сохраняет существующий `.env`, если он уже есть.

Заполните `.env`:

```dotenv
TODO_DB_HOST=localhost
TODO_DB_PORT=5432
TODO_DB_NAME=todo_db
TODO_DB_USER=todo_app
TODO_DB_PASSWORD=
TODO_JWT_SECRET=
```

В `TODO_DB_PASSWORD` укажите пароль роли `todo_app`. В `TODO_JWT_SECRET` укажите случайный ключ длиной не менее 64 символов. Сгенерировать подходящий ключ можно командой:

```bash
openssl rand -hex 32
```

Скопируйте результат в `TODO_JWT_SECRET`. Реальные пароли и ключи хранятся в локальном `.env`, который исключён из Git. В публикуемом `.env.example` поля секретов остаются пустыми.

### 5. Запустить API

С активным виртуальным окружением, из корня проекта:

```bash
fastapi dev backend/api.py
```

Базовый адрес API: [http://127.0.0.1:8000](http://127.0.0.1:8000).

Интерактивная документация Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Команда `fastapi dev` запускает сервер для локальной разработки.

## Маршруты

| Метод | Путь | Назначение | Требуется JWT |
| --- | --- | --- | --- |
| `POST` | `/register` | Создать аккаунт | Нет |
| `POST` | `/login` | Получить токен | Нет |
| `GET` | `/tasks` | Получить свои задачи | Да |
| `GET` | `/tasks/{task_id}` | Получить свою задачу | Да |
| `POST` | `/tasks` | Создать задачу | Да |
| `PATCH` | `/tasks/{task_id}/complete` | Отметить задачу выполненной | Да |

Фильтрация списка: `/tasks?status_filter=active` или `/tasks?status_filter=completed`.

## Пример работы через Swagger UI

1. Откройте `/docs` и создайте аккаунт через `POST /register`, указав собственные имя пользователя и пароль:

   ```json
   {
     "username": "example_user",
     "password": "your-account-password"
   }
   ```

2. Передайте те же данные в `POST /login`. В ответе будут `access_token` и `token_type` со значением `bearer`.

3. Нажмите **Authorize** в Swagger UI и вставьте значение `access_token`.

4. Создайте задачу через `POST /tasks`:

   ```json
   {
     "task": "Изучить JavaScript"
   }
   ```

5. Получите список через `GET /tasks`. Для отметки о выполнении передайте ID созданной задачи в `PATCH /tasks/{task_id}/complete`.

При обращении к API из другого клиента токен передаётся в HTTP-заголовке:

```http
Authorization: Bearer <access_token>
```

Если список пуст, API возвращает `[]`. Если задача отсутствует или принадлежит другому пользователю, API возвращает `404`. Отсутствующий или недействительный токен на защищённых маршрутах приводит к ответу `401`.

## Данные

| Таблица | Поля |
| --- | --- |
| `users` | `id`, `username`, `password_hash` |
| `tasks` | `id`, `task`, `status`, `user_id` |

`users.username` уникален. `tasks.user_id` ссылается на `users.id`. ID генерируются PostgreSQL автоматически. В текущем `schema.sql` генерация ID задач начинается с `1000`.

## Документация

- [FastAPI](https://fastapi.tiangolo.com/)
- [Psycopg 3](https://www.psycopg.org/psycopg3/docs/)
- [PostgreSQL 16: psql](https://www.postgresql.org/docs/16/app-psql.html)
- [PostgreSQL 16: GRANT](https://www.postgresql.org/docs/16/sql-grant.html)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)

## Подготовка README

Я маленький 16 летний болванчик поэтому этот README подготовлен с помощью ИИ, ибо мне очень дедлайн жмёт.
Сам проект я ручками писал, особой цели нет, просто хотел навыки набить.
