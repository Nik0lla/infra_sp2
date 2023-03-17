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

2. Перейдите в папку с кодом и создайте виртуальное окружение и активирйте его.
```bash
cd infra_sp2
cd api_yamdb
```
для windows-систем:
```bash
python -m venv venv
```
для *nix-систем:
```bash
python3 -m venv venv
```

3. Активируйте виртуальное окружение.

Для windows-систем:
```bash
source venv/Scripts/activate
```
для *nix-систем:
```bash
source venv/bin/activate
```

4. Переходим в папку с файлом docker-compose.yaml:
```bash
cd ..
cd infra
```

5. Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker-compose up -d --build
```

6. Выполняем миграции:
```bash
docker-compose exec web python manage.py makemigrations reviews
```
```bash
docker-compose exec web python manage.py migrate
```

7. Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

8. Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

9. Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

10. Останавливаем контейнеры:
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