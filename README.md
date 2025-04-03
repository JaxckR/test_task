# О приложении
Данное веб приложение предназначено для управления заказами в кафе.
Позволяет добавлять, редактировать, удалять и искать заказы, а также отслеживать их статус.

!! .env файл и остальные переменные не были скрыты лишь для удобства запуска для проверяющего в иной ситуации их необходимо скрыть<br>
Стек:
- Python 3.12
- Django 5
- PostgreSQL
- HTML/CSS + Bootstrap
- Docker + Docker compose

<hr>

# Инструкция по установке и запуску<br>

### Трудный способ(без использования docker)
У вас заранее должен быть установлен python и postgres, а также активировано виртуальное окружение
1. Скопируйте проект, находясь в любой удобной вам директории
```console
git clone https://github.com/JaxckR/test_task.git
```
2. Установите все зависимости
```console
pip install -r requirements.txt
```
3. Перейдите в папку src, создайте и примените миграции
```console
cd src
python manage.py makemigrations
python manage.py migrate
```
4. Запустите сервер
```console
python manage.py runserver
```
<br>

### Легкий способ(с использованием docker)
У вас должен быть установлен и запущен docker
1. Скопируйте проект, находясь в любой удобной вам директории
```console
git clone https://github.com/JaxckR/test_task.git
```
2. Запустите docker compose
```console
docker compose up --build
```
<br>
<hr>
<br>

# Документация

Поиск проводится по query параметру q<br>
/example/?q=search
<br><br>
API Endpoints:
- 'GET /api/v1/orders/' - получить список всех заказов
- 'POST /api/v1/orders/' - создать новый заказ
- 'GET /api/v1/orders/{id}/' - получить информацию о заказе
- 'PATCH /api/v1/orders/{id}/' - частично обновить сведения о заказе
- 'PUT /api/v1/orders/{id}/' - полностью обновить сведения о заказе
- 'DELETE /api/v1/orders/{id}/' - удалить сведения о заказе
- 'GET /api/v1/orders/{id}/items/' - получить информацию о позициях заказа
- 'PATCH /api/v1/orders/{id}/items/' - изменить информацию о позициях заказа
