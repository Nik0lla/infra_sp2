# Yamdb API
Проект REST API для сервиса YaMDb предназначен для сбора отзывов о книгах, фильмах и музыке.

## Описание

Проект YaMDb собирает отзывы пользователей на произведения.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Список категорий  может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

**Документация:**  <http://127.0.0.1:8000/redoc>

----

## Установка

Для запуска приложения проделайте следующие шаги:

1. Склонируйте репозиторий:
```bash
git clone git@github.com:Nik0lla/infra_sp2.git
```

2. Переходим в папку с файлом docker-compose.yaml:
```bash
cd infra_sp2/infra/
```

3. Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker-compose up -d --build
```

4. Выполняем миграции:
```bash
docker-compose exec web python manage.py makemigrations reviews
```
```bash
docker-compose exec web python manage.py migrate
```

5. Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

7. Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

8. Останавливаем контейнеры:
```bash
docker-compose down -v
```

### Шаблон наполнения .env.sample расположенный по пути infra/.env.sample
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```