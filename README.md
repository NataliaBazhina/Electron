            Онлайн-платформа торговой сети электроники

это приложение для управления иерархической структурой торговой сети по продаже электроники. 
Платформа предоставляет API-интерфейс и админ-панель для управления объектами сети.

                        Основные функции

Иерархическая структура из трех уровней

CRUD операции через REST API

Админ-панель с расширенными функциями управления

Аутентификация через JWT токены

Права доступа только для активных сотрудников

Валидация бизнес-правил сети

                        Технологический стек

Python 3.8+

Django 3+

Django REST Framework 3.10+

PostgreSQL 10+

Simple JWT для аутентификации

Django Filter для фильтрации

                        Установка и запуск
1. Клонирование репозитория

 git clone git@github.com:NataliaBazhina/Electron.git

cd electron

2. Создание виртуального окружения

python -m venv venv

source venv/bin/activate  # Linux/Mac

venv\Scripts\activate  # Windows

3. Установка зависимостей

pip install -r requirements.txt

4. Настройка базы данных

Создайте файл .env в корневой директории:

SECRET_KEY=your-secret-key

DB_NAME=electron

DB_USER=your_db_user

DB_PASSWORD=your_db_password

DB_HOST=localhost

DB_PORT=5432

5. Миграции и суперпользователь

python manage.py migrate

python manage.py csu

6. Запуск сервера

python manage.py runserver

                            Структура API
Основные endpoints:

GET/POST /networks/ - список всех звеньев сети

GET/PUT/PATCH/DELETE /networks/{id}/ - конкретное звено

POST /login/ - получение JWT токена

POST /token/refresh/ - обновление токена

Админ-панель по адресу: /admin/
Особенности админ-панели:

Кликабельная ссылка на объект поставщика

Фильтрация объектов по названию города

Очистка задолженности 

Иерархическое отображение 


                    Бизнес-правила и валидация


Правила иерархии:

Уровень 0: Завод (не может иметь поставщика)

Розничная сеть и ИП могут быть как уровнем 1, так и уровнем 2.

                        Фильтрация и поиск
Доступные фильтры:

http://localhost:8000/networks/?country=Россия - фильтр по стране

http://localhost:8000/networks/?search=Москва - поиск по названию и городу


                        Права доступа

Только активные сотрудники имеют доступ к API

JWT аутентификация обязательна для всех endpoints

Примеры использования
Получение токена:
bash

curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123qwe"}'

Создание нового звена:
bash

curl -X POST http://localhost:8000/networks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Розничный магазин",
    "type": 1,
    "email": "shop@example.com",
    "country": "Россия",
    "city": "Москва",
    "street": "Тверская",
    "house_number": "10",
    "product_name": "Ноутбук",
    "product_model": "XPS 13",
    "product_release_date": "2024-01-01",
    "supplier": 1
  }'


