# Django Project Management Application

## Описание

Это приложение предназначено для управления проектами и задачами, разработанное на Django. Оно включает в себя функционал для работы с пользователями, проектами и задачами, а также систему аутентификации.

## Основные функции

### Пользователи и аутентификация

- **Регистрация**: Пользователи могут создавать аккаунты с уникальными именами и паролями.
- **Профиль**: Каждый пользователь имеет профиль с информацией о себе, включая имя, фамилию, аватар и роль на платформе.
- **Аутентификация**: Поддержка входа в систему с проверкой учетных данных.

### Управление проектами

- **CRUD операции**: Возможность создавать, читать, обновлять и удалять проекты.
- **Участники**: Добавление и удаление пользователей из проектов, а также назначение ролей.
- **Свойства проекта**: Каждый проект имеет название, описание, даты создания и обновления, а также статус (активен или архивирован).
- **Фильтрация и сортировка**: Проекты можно сортировать по различным критериям, таким как дата создания и название.

### Управление задачами

- **CRUD операции**: Создание, чтение, обновление и удаление задач.
- **Свойства задачи**: Задачи содержат название, описание, ссылки на проект и исполнителя, статус, приоритет, даты создания и обновления, а также срок выполнения.
- **Комментарии**: Возможность добавления, редактирования и удаления комментариев к задачам.
- **Фильтрация и сортировка**: Задачи можно сортировать и фильтровать по различным параметрам, включая статус и приоритет.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/EnterNick/Task-tracker.git
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```

3. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Примените миграции:
   ```bash
   cd ./Task-tracker/main/
   python manage.py migrate
   ```

5. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

## Примечание: 
- перед использованием необходимо запустить сервер PostgreSQL на порту 5432 или использовать Docker для этих целей.

## Испольование Docker:

1. Установите проект по инструкции выше (Примечание: Избегайте последних двух пунктов)

2. Перейдите в директорию проекта:
  ```bash
  cd ./Task-tracker/
  ```

3. Используйте docker для запуска контейнеров:
```bash
docker-compose up --build -d
```

4. Для остановки работы проекта:
```bash
docker-compose down
```

## Важно: Если вы работаете на Windows, убедитесь, что запущен docker engine. Для этого необходимо просто запустить приложение Docker Desktop.

## Использование

- Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/`.
- Зарегистрируйтесь или войдите в систему для начала работы с приложением.

