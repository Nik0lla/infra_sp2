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
python -m pip install --upgrade pip
```
для *nix-систем:
```bash
source venv/bin/activate
python3 -m pip install --upgrade pip
```

4. Установите необходимые пакеты.

Для windows-систем:
```bash
python -m pip install -r requirements.txt
```
для *nix-систем:
```bash
python3 -m pip install -r requirements.txt
```

5. Переходим в папку с файлом docker-compose.yaml:
```bash
cd ..
cd infra
```

6. Поднимаем контейнеры (infra_db_1, infra_web_1, infra_nginx_1):
```bash
docker-compose up -d --build
```

7. Выполняем миграции:
```bash
docker-compose exec web python manage.py makemigrations reviews
```
```bash
docker-compose exec web python manage.py migrate
```

8. Создаем суперпользователя:
```bash
docker-compose exec web python manage.py createsuperuser
```

9. Србираем статику:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

10. Создаем дамп базы данных (нет в текущем репозитории):
```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

11. Останавливаем контейнеры:
```bash
docker-compose down -v
```

### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```